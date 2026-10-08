# Báo cáo Day 6: Đánh Giá Chất Lượng Chiếu LiDAR - Camera & Độ Nhạy Sai Lệch Calibration

- **Họ tên:** Lâm Quang Anh Quân
- **MSSV:** 2A202602467
- **Lớp:** AI20K-T4
- **Link repo:** https://github.com/awun0105/LamQuangAnhQuan-2A202602467-Track4-Day21.git
- **Topic:** A — LiDAR-camera projection QA
- **Dataset:** data/kitti_mini, data/nuscenes_mini_subset, data/synthetic
- **Các frame đã dùng:** 000011, 000004, 000021 (KITTI); scene-0103_010 (nuScenes); 000000 (synthetic)

> Báo cáo đánh giá độ nhạy của phép chiếu LiDAR-Camera trước các sai lệch ngoại suy (extrinsic calibration drift) và đề xuất cơ chế giám sát tự động.

## 1. Claim

Độ lệch góc xoay Yaw $\ge 1.0^\circ$ của cảm biến LiDAR làm suy giảm hơn $15\%$ tỷ lệ điểm LiDAR rơi đúng vào hộp 2D Bounding Box của xe hơi ở khoảng cách trên $25\,\text{m}$, và hiện tượng lệch này có thể được phát hiện tự động bằng chỉ số tương thích biên cạnh (Edge Alignment Score) với ngưỡng suy giảm vượt quá $20\%$.

## 2. Evidence

Bảng hoặc plot số liệu, kèm ảnh/video demo. Ghi rõ đường dẫn file trong `results/`.

| Cấu hình / mức perturb | Metric 1 | Metric 2 | Ghi chú |
|---|---|---|---|
| [ĐIỀN] | | | |

![demo](../results/figures/[ĐIỀN].png)

## 3. Failure case

Nêu khi nào hệ thống hoặc phương pháp fail, vì sao fail, và liên hệ tới lớp nào trong 6 lớp debug: I/O, Geometry, Time, Preprocess, Model, Metric.

![failure](../results/figures/fail_[ĐIỀN].png)

[ĐIỀN]

## 4. Khuyến nghị nếu triển khai thật

Use-case cụ thể (ADAS / robot / drone), trade-off và bước tiếp theo.

[ĐIỀN]

## 5. Cách chạy lại

Các lệnh tái tạo lại toàn bộ kết quả từ repo sạch.

```bash
[ĐIỀN]
```

## 6. Khai báo sử dụng AI

Ghi rõ đã dùng công cụ AI nào, dùng vào việc gì, và bạn đã tự kiểm chứng kết quả đó bằng cách nào. Nếu không dùng AI, ghi "Không sử dụng". Xem quy định ở `RULES.md` mục 2.

| Công cụ | Dùng cho việc gì | Bạn đã kiểm chứng thế nào |
|---|---|---|
| [ĐIỀN] | | |
