"""So sánh hành vi phép chiếu giữa KITTI 64-beam và nuScenes 32-beam (Bonus B5).

Lưu kết quả ra results/kitti_vs_nuscenes.csv.
"""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np

from starter.datasets import load_frame
from starter.projection import perturb_extrinsic, project_velo_to_image


def compare_datasets() -> list[dict[str, str | float]]:
    configs = [
        ("KITTI 64-beam", "data/kitti_mini", "000011", {}),
        ("nuScenes 32-beam (với bù chuyển động)", "data/nuscenes_mini_subset", "scene-0103_010", {"use_ego_motion": True}),
        ("nuScenes 32-beam (KHÔNG bù chuyển động)", "data/nuscenes_mini_subset", "scene-0103_010", {"use_ego_motion": False}),
    ]

    yaw_levels = [0.0, 1.0, 2.0, 3.0]
    rows = []

    for name, root, fid, kwargs in configs:
        fr = load_frame(root, fid, **kwargs)
        pts = fr["points"]
        total_pts = len(pts)
        H, W = fr["image"].shape[:2]

        for yaw in yaw_levels:
            calib_p = perturb_extrinsic(fr["calib"], yaw_deg=yaw)
            uv, depth, mask = project_velo_to_image(pts, calib_p, fr["image"].shape)
            inside_fov = int(mask.sum())
            fov_pct = (inside_fov / total_pts) * 100.0

            rows.append({
                "dataset_config": name,
                "frame_id": fid,
                "yaw_deg": yaw,
                "total_points": total_pts,
                "points_inside_fov": inside_fov,
                "fov_retention_pct": round(fov_pct, 2),
                "image_resolution": f"{W}x{H}",
            })

    return rows


def main() -> None:
    rows = compare_datasets()
    out_csv = Path("results/kitti_vs_nuscenes.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"=== ĐÃ XUẤT SO SÁNH KITTI VS NUSCENES (BONUS B5) ===")
    for r in rows:
        print(f"[{r['dataset_config']}] Yaw {r['yaw_deg']}°: FOV pts={r['points_inside_fov']}/{r['total_points']} ({r['fov_retention_pct']}%)")
    print(f"-> Lưu vào {out_csv}")


if __name__ == "__main__":
    main()
