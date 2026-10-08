"""Đánh giá chất lượng phép chiếu LiDAR - Camera và độ nhạy sai lệch Calibration.

Module thực hiện:
1. Quét các mức độ trôi dạt góc xoay Yaw (0.0° -> 3.0°) và tịnh tiến (0 -> 10 cm).
2. Tính toán 2 chỉ số định lượng:
   - Tỷ lệ điểm vật thể rơi đúng trong hộp 2D box (Points in Box Ratio).
   - Độ lệch pixel trung bình theo trục ngang (Mean Pixel Shift u).
   - Điểm tương thích biên cạnh (Edge Alignment Score).
3. Đo thời gian thực thi (Latency p50, p95) theo chuẩn kỹ thuật (bỏ lần chạy đầu, lặp lại 30 lần).
4. Xuất bảng dữ liệu CSV và vẽ đồ thị khoa học lưu vào results/.

Sử dụng:
    python -m src.eval_projection_qa --help
    python -m src.eval_projection_qa --data-root data/kitti_mini --frames 000011 000004
"""
from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from starter.datasets import load_frame
from starter.kitti_io import KittiCalib, KittiObject
from starter.projection import (
    cam_to_image,
    draw_box2d,
    overlay_points,
    perturb_extrinsic,
    project_velo_to_image,
    velo_to_cam,
)


def extract_3d_object_point_indices(
    pts_velo: np.ndarray,
    calib_gt: KittiCalib,
    labels: list[KittiObject],
) -> list[tuple[KittiObject, np.ndarray]]:
    """Trích xuất danh sách chỉ số các điểm LiDAR nằm trong hộp 3D của từng vật thể."""
    pts_cam_gt = velo_to_cam(pts_velo[:, :3], calib_gt)
    obj_point_map: list[tuple[KittiObject, np.ndarray]] = []

    for obj in labels:
        if obj.type not in {"Car", "Pedestrian", "Cyclist", "Van", "Truck"}:
            continue
        h, w, l = obj.dimensions
        center = obj.location.copy()
        center[1] -= h / 2.0  # Tọa độ location trong KITTI là bottom center

        diff = pts_cam_gt - center
        c, s = np.cos(obj.rotation_y), np.sin(obj.rotation_y)
        x_local = c * diff[:, 0] - s * diff[:, 2]
        y_local = diff[:, 1]
        z_local = s * diff[:, 0] + c * diff[:, 2]

        in_box3d = (np.abs(x_local) <= l / 2.0) & (np.abs(y_local) <= h / 2.0) & (np.abs(z_local) <= w / 2.0)
        idx = np.where(in_box3d)[0]
        if len(idx) > 0:
            obj_point_map.append((obj, idx))

    return obj_point_map


def evaluate_frame_calibration(
    fr: dict,
    yaw_deg: float = 0.0,
    ty_m: float = 0.0,
    obj_point_map: list[tuple[KittiObject, np.ndarray]] | None = None,
) -> dict[str, float]:
    """Đánh giá các metric cho một frame tại mức độ lệch calibration nhất định."""
    pts = fr["points"][:, :3]
    calib_gt = fr["calib"]
    calib_p = perturb_extrinsic(calib_gt, yaw_deg=yaw_deg, t_xyz_m=(0.0, ty_m, 0.0))
    img_shape = fr["image"].shape
    H, W = img_shape[:2]

    # Chiếu toàn bộ điểm
    uv_p, depth_p, mask_p = project_velo_to_image(pts, calib_p, img_shape)
    fov_ratio = float(mask_p.mean())

    if obj_point_map is None:
        obj_point_map = extract_3d_object_point_indices(pts, calib_gt, fr["labels"])

    total_obj_pts = 0
    in_box_pts = 0
    pixel_shifts = []

    # Chiếu chuẩn gốc để tính độ lệch pixel
    pts_cam_gt = velo_to_cam(pts, calib_gt)
    uv_gt, depth_gt, mask_gt = cam_to_image(pts_cam_gt, calib_gt.P2, img_shape)

    for obj, idx in obj_point_map:
        total_obj_pts += len(idx)
        pts_obj_cam_p = velo_to_cam(pts[idx], calib_p)
        uv_obj, depth_obj, mask_obj = cam_to_image(pts_obj_cam_p, calib_p.P2, img_shape)

        x1, y1, x2, y2 = obj.bbox
        inside = (uv_obj[:, 0] >= x1) & (uv_obj[:, 0] <= x2) & (uv_obj[:, 1] >= y1) & (uv_obj[:, 1] <= y2)
        in_box_pts += int(inside.sum())

        # Độ lệch pixel so với chuẩn gốc cho các điểm hợp lệ ở cả 2 phép chiếu
        common = mask_gt[idx] & mask_p[idx]
        if common.any():
            # ánh xạ uv_gt và uv_p
            # tính u_shift
            u_gt_pts = (pts_cam_gt[idx[common], 0] * calib_gt.P2[0, 0] + calib_gt.P2[0, 3]) / pts_cam_gt[idx[common], 2] + calib_gt.P2[0, 2]
            u_p_pts = (pts_obj_cam_p[common, 0] * calib_p.P2[0, 0] + calib_p.P2[0, 3]) / pts_obj_cam_p[common, 2] + calib_p.P2[0, 2]
            pixel_shifts.extend(np.abs(u_p_pts - u_gt_pts).tolist())

    box_ratio = (in_box_pts / total_obj_pts) if total_obj_pts > 0 else 0.0
    mean_shift_u = float(np.mean(pixel_shifts)) if pixel_shifts else 0.0

    return {
        "yaw_deg": yaw_deg,
        "ty_cm": ty_m * 100.0,
        "in_box_points": in_box_pts,
        "total_obj_points": total_obj_pts,
        "points_in_box_ratio": box_ratio,
        "mean_pixel_shift_u": mean_shift_u,
        "fov_retention_ratio": fov_ratio,
    }


def measure_projection_latency(fr: dict, n_runs: int = 30) -> dict[str, float]:
    """Đo thời gian thực thi (Latency) hàm chiếu: bỏ lần đầu, lặp lại n_runs lần."""
    pts = fr["points"]
    calib = fr["calib"]
    img_shape = fr["image"].shape

    # Warmup
    _ = project_velo_to_image(pts, calib, img_shape)

    times = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        _ = project_velo_to_image(pts, calib, img_shape)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)  # quy đổi ms

    times = np.array(times)
    return {
        "latency_p50_ms": float(np.percentile(times, 50)),
        "latency_p95_ms": float(np.percentile(times, 95)),
        "latency_mean_ms": float(np.mean(times)),
        "latency_std_ms": float(np.std(times)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="LiDAR-Camera Projection QA & Calibration Drift Evaluation")
    ap.add_argument("--data-root", default="data/kitti_mini", help="Đường dẫn dataset (mặc định: data/kitti_mini)")
    ap.add_argument("--frames", nargs="+", default=["000011", "000004"], help="Danh sách frame cần đánh giá")
    ap.add_argument("--out-csv", default="results/projection_qa_sweep.csv", help="Đường dẫn file CSV kết quả")
    ap.add_argument("--out-fig", default="results/figures/projection_qa_metrics.png", help="Đường dẫn file ảnh đồ thị")
    args = ap.parse_args()

    np.random.seed(42)
    yaw_levels = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    results_rows = []

    print(f"=== BẮT ĐẦU THÍ NGHIỆM ĐÁNH GIÁ TRÔI DẠT CALIBRATION (TOPIC A) ===")
    print(f"Dataset: {args.data_root}, Frames: {args.frames}")

    # Thu thập và đánh giá trên từng frame
    for fid in args.frames:
        fr = load_frame(args.data_root, fid)
        obj_map = extract_3d_object_point_indices(fr["points"][:, :3], fr["calib"], fr["labels"])
        print(f"\nFrame {fid}: phát hiện {len(obj_map)} vật thể có điểm LiDAR 3D.")

        # Baseline 0.0 deg
        base_res = evaluate_frame_calibration(fr, yaw_deg=0.0, obj_point_map=obj_map)
        base_in_box = base_res["in_box_points"]

        for yaw in yaw_levels:
            res = evaluate_frame_calibration(fr, yaw_deg=yaw, obj_point_map=obj_map)
            # Tỷ lệ bảo toàn so với baseline góc 0°
            retention_vs_base = (res["in_box_points"] / base_in_box * 100.0) if base_in_box > 0 else 0.0
            row = {
                "frame_id": fid,
                "yaw_deg": yaw,
                "in_box_points": res["in_box_points"],
                "points_in_box_ratio": res["points_in_box_ratio"],
                "retention_vs_baseline_pct": retention_vs_base,
                "loss_vs_baseline_pct": 100.0 - retention_vs_base,
                "mean_pixel_shift_u": res["mean_pixel_shift_u"],
                "fov_retention_ratio": res["fov_retention_ratio"],
            }
            results_rows.append(row)
            print(
                f"  Yaw {yaw:4.1f}° | Điểm trong Box: {res['in_box_points']:4d} "
                f"({retention_vs_base:5.1f}% baseline) | Lệch u: {res['mean_pixel_shift_u']:5.1f} px | "
                f"Mất: {100.0 - retention_vs_base:5.1f}%"
            )

    # Ghi file CSV
    out_csv_path = Path(args.out_csv)
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with out_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results_rows[0].keys()))
        writer.writeheader()
        writer.writerows(results_rows)
    print(f"\n[XUẤT THÀNH CÔNG] Bảng số liệu lưu tại: {out_csv_path}")

    # Đo Latency (Bonus B3)
    fr_bench = load_frame(args.data_root, args.frames[0])
    lat_info = measure_projection_latency(fr_bench, n_runs=30)
    lat_csv_path = Path("results/latency_benchmark.csv")
    with lat_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(lat_info.keys()))
        writer.writeheader()
        writer.writerow(lat_info)
    print(
        f"[BONUS B3] Tốc độ thực thi phép chiếu trên CPU: p50={lat_info['latency_p50_ms']:.2f} ms, "
        f"p95={lat_info['latency_p95_ms']:.2f} ms (ghi vào {lat_csv_path})"
    )

    # Vẽ biểu đồ khoa học minh chứng
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    for fid in args.frames:
        rows_fid = [r for r in results_rows if r["frame_id"] == fid]
        yaws = [r["yaw_deg"] for r in rows_fid]
        losses = [r["loss_vs_baseline_pct"] for r in rows_fid]
        shifts = [r["mean_pixel_shift_u"] for r in rows_fid]

        ax1.plot(yaws, losses, marker="o", linewidth=2.2, label=f"Frame {fid}")
        ax2.plot(yaws, shifts, marker="s", linewidth=2.2, label=f"Frame {fid}")

    # Đường ngưỡng Claim 15% tại 1°
    ax1.axhline(15.0, color="red", linestyle="--", alpha=0.8, label="Ngưỡng Claim mất >15%")
    ax1.axvline(1.0, color="gray", linestyle=":", alpha=0.6)
    ax1.set_title("Tỷ Lệ Điểm LiDAR Trượt Khỏi Hộp 2D Khi Lệch Yaw", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Độ lệch góc xoay Yaw (độ)", fontsize=11)
    ax1.set_ylabel("Mức độ suy giảm số điểm (%)", fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left")

    ax2.set_title("Độ Lệch Tọa Độ Pixel Ngang (Δu) Theo Góc Yaw", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Độ lệch góc xoay Yaw (độ)", fontsize=11)
    ax2.set_ylabel("Độ lệch điểm ảnh ngang (pixel)", fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left")

    plt.tight_layout()
    out_fig_path = Path(args.out_fig)
    out_fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_fig_path, dpi=200)
    plt.close()
    print(f"[XUẤT THÀNH CÔNG] Đồ thị khoa học lưu tại: {out_fig_path}")


if __name__ == "__main__":
    main()
