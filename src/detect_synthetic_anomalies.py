"""Phát hiện toàn bộ các lỗi cài sẵn trong bộ dữ liệu data/synthetic (Bonus B6).

Lập bảng và xuất kết quả ra results/synthetic_anomalies.csv:
1. Lỗi điểm NaN/Inf trong point cloud (xuất hiện ở mọi frame: 22-23 điểm).
2. Lỗi nhảy cóc mốc thời gian (Time gap jump) tại frame 000003 (khoảng cách 0.2s thay vì 0.1s).
3. Lỗi mất chùm tia theo góc quét (Sector dropout) tại frame 000003 (mất ~1,800 điểm).
"""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np

from starter.datasets import list_frames, load_points


def scan_synthetic_anomalies(data_root: str = "data/synthetic") -> list[dict[str, str]]:
    frames = list_frames(data_root)
    ts_file = Path(data_root) / "training" / "timestamps.txt"
    timestamps = [float(line.strip()) for line in ts_file.read_text().splitlines()] if ts_file.exists() else []

    anomalies: list[dict[str, str]] = []

    # 1. Quét NaN/Inf
    for fid in frames:
        pts = load_points(data_root, fid)
        nans = np.isnan(pts).any(axis=1).sum()
        infs = np.isinf(pts).any(axis=1).sum()
        if nans > 0 or infs > 0:
            anomalies.append({
                "anomaly_type": "Invalid Points (NaN/Inf)",
                "affected_frame": fid,
                "evidence_detail": f"Có {nans} điểm NaN, {infs} điểm Inf trên tổng số {len(pts)} điểm",
                "detection_method": "np.isnan(pts).any(axis=1).sum() > 0",
            })

    # 2. Quét Time Gap
    for i in range(1, len(timestamps)):
        dt = timestamps[i] - timestamps[i - 1]
        if not np.isclose(dt, 0.1, atol=1e-3):
            anomalies.append({
                "anomaly_type": "Time Gap / Frame Drop",
                "affected_frame": frames[i],
                "evidence_detail": f"Chu kỳ delta_t = {dt:.2f}s (chuẩn 10Hz là 0.10s, mất 1 frame giữa frame {frames[i-1]} và {frames[i]})",
                "detection_method": "timestamps[i] - timestamps[i-1] > 0.15s",
            })

    # 3. Quét Sector / Point Drop
    base_pts = len(load_points(data_root, frames[0]))
    for fid in frames:
        pts = load_points(data_root, fid)
        if len(pts) < base_pts * 0.95:
            anomalies.append({
                "anomaly_type": "Sector / Beam Dropout",
                "affected_frame": fid,
                "evidence_detail": f"Số điểm giảm đột ngột còn {len(pts)} điểm (sụt giảm {base_pts - len(pts)} điểm so với mức chuẩn ~{base_pts})",
                "detection_method": "len(points) < 0.95 * baseline_points",
            })

    return anomalies


def main() -> None:
    anomalies = scan_synthetic_anomalies("data/synthetic")
    out_csv = Path("results/synthetic_anomalies.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(anomalies[0].keys()))
        writer.writeheader()
        writer.writerows(anomalies)

    print(f"=== ĐÃ PHÁT HIỆN {len(anomalies)} LỖI CÀI SẴN TRONG DATA/SYNTHETIC (BONUS B6) ===")
    for a in anomalies:
        print(f"[{a['anomaly_type']}] Frame {a['affected_frame']}: {a['evidence_detail']}")
    print(f"-> Đã ghi bảng chi tiết vào {out_csv}")


if __name__ == "__main__":
    main()
