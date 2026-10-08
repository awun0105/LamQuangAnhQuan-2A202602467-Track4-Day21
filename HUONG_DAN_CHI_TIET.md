# CẨM NANG TOÀN DIỆN: ĐÁM MÂY ĐIỂM 3D & CHIẾU ĐỒNG BỘ LIDAR - CAMERA
## Bài Lab Mini-Project (Track 4 · Ngày 21) — 3D From Point Clouds & LiDAR-Camera Projection

> **Tác giả:** Lâm Quang Anh Quân — MSSV: `2A202602467`  
> **Kho mã nguồn:** `LamQuangAnhQuan-2A202602467-Track4-Day21`  
> **Mục tiêu học thuật:** Làm chủ nguyên lý gốc (First-Principles Thinking) về đám mây điểm 3D (Point Cloud), phép chiếu hình học quang học từ LiDAR sang Camera, kỹ thuật kiểm định căn chỉnh (Calibration QA), phân tích lỗi theo 6 tầng kiến trúc hệ thống xe tự hành, và hoàn thành xuất sắc bài lab với mục tiêu **100/100 điểm chính thức + 10/10 điểm thưởng (Bonus)**.

---

## MỤC LỤC
1. [Tổng Quan Về Bài Lab & Lộ Trình 120 Phút](#1-tổng-quan-về-bài-lab--lộ-trình-120-phút)
2. [Nguyên Lý Gốc: Tại Sao Cần Kết Hợp LiDAR & Camera?](#2-nguyên-lý-gốc-tại-sao-cần-kết-hợp-lidar--camera)
3. [Giải Phẫu Hình Học: Chuỗi Phép Chiếu Từ Điểm 3D Lên Điểm Ảnh 2D](#3-giải-phẫu-hình-học-chuỗi-phép-chiếu-từ-điểm-3d-lên-điểm-ảnh-2d)
4. [Hướng Dẫn Cài Đặt 2 Hàm Cốt Lõi Trong `starter/projection.py`](#4-hướng-dẫn-cài-đặt-2-hàm-cốt-lõi-trong-starterprojectionpy)
5. [Chiến Lược Chọn Đề Tài Đạt Điểm Tối Đa: Topic A (Projection QA)](#5-chiến-lược-chọn-đề-tài-đạt-điểm-tối-đa-topic-a-projection-qa)
6. [Phương Pháp Luận Phân Tích Lỗi Qua 6 Tầng Debug Hệ Thống](#6-phương-pháp-luận-phân-tích-lỗi-qua-6-tầng-debug-hệ-thống)
7. [Bí Kíp Săn Trọn 10 Điểm Thưởng (Bonus B1 Đến B6)](#7-bí-kíp-săn-trọn-10-điểm-thưởng-bonus-b1-đến-b6)
8. [Bài Học Triển Khai Thực Tế Trong Xe Tự Hành & Robot Công Nghiệp](#8-bài-học-triển-khai-thực-tế-trong-xe-tự-hành--robot-công-nghiệp)
9. [Checklist Hoàn Thiện Báo Cáo `report/REPORT.md` & Nộp Bài](#9-checklist-hoàn-thiện-báo-cáo-reportreportmd--nộp-bài)

---

## 1. TỔNG QUAN VỀ BÀI LAB & LỘ TRÌNH 120 PHÚT

### 1.1 Tinh thần cốt lõi của bài lab
Khác với các bài tập thông thường chỉ yêu cầu chạy lại mô hình AI có sẵn, bài lab này đánh giá năng lực của một **Kỹ sư Thị giác máy tính & Xe tự hành thực chiến (Computer Vision & Autonomous Systems Engineer)**:
- Không chạy đua cài đặt mô hình phức tạp hay viết code dài dòng.
- Đánh giá khả năng biến một vấn đề thực tế mơ hồ (ví dụ: *"Nếu giá đỡ cảm biến bị va quẹt làm lệch 1 độ thì hệ thống lái tự động bị ảnh hưởng thế nào?"*) thành một **thí nghiệm khoa học có kiểm soát**, đo đạc bằng số liệu định lượng và chứng minh bằng hình ảnh trực quan.
- Bắt buộc phải tìm ra **trường hợp thất bại (Failure Case)** và giải thích đúng nguyên nhân gốc rễ theo các tầng kỹ thuật của xe.

### 1.2 Lộ trình 120 phút qua 6 Checkpoint (CP0 – CP6)

| Mốc thời gian | Checkpoint | Công việc trọng tâm | Sản phẩm nghiệm thu bắt buộc |
| :---: | :---: | :--- | :--- |
| **Trước giờ lab** | **CP0** | Clone repo, tạo venv, kiểm tra dữ liệu bằng `verify_data.py`. | Môi trường sẵn sàng, dữ liệu đủ 100%. |
| **0:00 – 0:15** | **CP1** | Chọn Topic (khuyên dùng Topic A), viết câu khẳng định kỹ thuật (Claim) có thể kiểm chứng. | Mục 1 của `report/REPORT.md` có claim rõ ràng. |
| **0:15 – 0:50** | **CP2** | Viết 2 hàm TODO trong `projection.py`, chạy ảnh overlay đầu tiên. | Ảnh overlay đầu tiên trong `results/figures/`. |
| **0:50 – 1:25** | **CP3** | Chạy thí nghiệm chính quét tối thiểu 3 mức lệch calibration, xuất bảng CSV và đồ thị. | File `results/*.csv` và biểu đồ minh họa. |
| **1:25 – 1:45** | **CP4** | Tìm ít nhất 1 ca thất bại (Failure case), lưu ảnh `fail_*.png`, phân tích nguyên nhân. | Mục 3 của `REPORT.md` kèm ảnh minh họa lỗi. |
| **1:45 – 2:00** | **CP5** | Hoàn thiện toàn bộ 6 mục của `REPORT.md`, chạy `check_submission.py` đạt [PASS] 100%, commit & push. | Repo sạch sẽ, sẵn sàng nộp. |
| **2:00 – 2:20** | **CP6** | Trình bày trước lớp trong 3 phút (nếu được giảng viên gọi ngẫu nhiên). | Slide / báo cáo mạch lạc, trả lời tự tin. |

---

## 2. NGUYÊN LÝ GỐC: TẠI SAO CẦN KẾT HỢP LIDAR & CAMERA?

### 2.1 Bảng so sánh đặc tính vật lý của 2 loại cảm biến

| Đặc tính | Camera (Quang học 2D) | LiDAR (Cảm biến chùm tia Laser 3D) |
| :--- | :--- | :--- |
| **Bản chất đo đạc** | Cường độ ánh sáng phản xạ trên cảm biến CMOS/CCD. | Thời gian bay của xung laser (Time-of-Flight: $d = \frac{c \cdot \Delta t}{2}$). |
| **Thông tin thu được** | Màu sắc RGB, kết cấu bề mặt, chữ viết biển báo, vạch kẻ đường. | Tọa độ không gian 3 chiều $[x, y, z]$ chính xác đến từng milimét + cường độ phản xạ (intensity). |
| **Điểm yếu chí mạng** | Mất hoàn toàn thông tin độ sâu thực tế (Scale Ambiguity), bị mù khi trời tối, ngược sáng hoặc sương mù dày. | Đám mây điểm thưa thớt (sparse), không đọc được chữ, khó phân biệt giữa túi nilon và tảng đá nhỏ. |
| **Tính cấu trúc** | Ma trận ảnh 2 chiều có thứ tự liên tục $[H \times W \times 3]$. | Tập hợp các điểm rời rạc bất quy tắc (unordered point set), mật độ giảm nhanh theo khoảng cách ($1/d^2$). |

```
[Camera: Nhận diện "Đó là một chiếc xe hơi", nhưng không biết cách bao xa]
                              ➕
[LiDAR: Đo chuẩn "Có vật cản cách đúng 23.45 mét", nhưng không biết là vật gì]
                              ⬇
[HỢP NHẤT: "Có một chiếc xe hơi đang ở đúng khoảng cách 23.45 mét!"]
```

---

### 2.2 Sự khác biệt về hệ quy chiếu tọa độ giữa các thiết bị
Để đưa một điểm từ LiDAR sang điểm ảnh Camera, điều đầu tiên là phải nắm vững **quy ước trục tọa độ**:

```
1. Hệ trục LiDAR KITTI (Velodyne):
   - Trục X: Hướng thẳng về phía trước đầu xe
   - Trục Y: Hướng sang bên trái xe
   - Trục Z: Hướng thẳng đứng lên trời

2. Hệ trục Camera chuẩn (Rectified Camera Frame):
   - Trục X: Hướng sang bên phải ảnh
   - Trục Y: Hướng thẳng đứng xuống dưới
   - Trục Z: Hướng thẳng về phía trước tầm nhìn (trục quang học / độ sâu)

3. Hệ trục LiDAR nuScenes:
   - Trục X: Hướng sang bên phải xe
   - Trục Y: Hướng thẳng về phía trước đầu xe
   - Trục Z: Hướng thẳng đứng lên trời
```

> **Cảnh báo sai lầm kinh điển:** Nhiều người nghĩ trục Z của LiDAR cũng là trục Z của Camera. Thực tế, trục Z của Camera là **khoảng cách nhìn thẳng về phía trước**, trong khi ở LiDAR nó lại là **chiều cao hướng lên trời**! Nếu không qua phép biến đổi tọa độ, toàn bộ hình ảnh chiếu sẽ bị lộn ngược và văng lên bầu trời.

---

## 3. GIẢI PHẪU HÌNH HỌC: CHUỖI PHÉP CHIẾU TỪ ĐIỂM 3D LÊN ĐIỂM ẢNH 2D

Mọi bài toán chiếu điểm LiDAR lên ảnh camera đều xoay quanh phương trình chiếu trung tâm:

$$s \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{P}_2 \cdot \mathbf{R}_0^{\text{rect}} \cdot \mathbf{T}_{\text{velo}\to\text{cam}} \cdot \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

Hay viết gọn lại qua ma trận gộp $\mathbf{T}_{\text{cam}\_\text{velo}} = \mathbf{R}_0^{\text{rect}} \cdot \mathbf{T}_{\text{velo}\to\text{cam}}$:

$$\mathbf{x}_{\text{cam}} = \mathbf{T}_{\text{cam}\_\text{velo}} \cdot \mathbf{x}_{\text{velo}}$$

$$s \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{P}_2 \cdot \begin{bmatrix} x_{\text{cam}} \\ y_{\text{cam}} \\ z_{\text{cam}} \\ 1 \end{bmatrix}$$

---

### 3.1 Giai đoạn 1: Biến đổi từ tọa độ LiDAR sang Camera (`velo_to_cam`)

$$\mathbf{x}_{\text{cam}}^{\text{homo}} = \mathbf{T}_{\text{cam}\_\text{velo}} \cdot \mathbf{x}_{\text{velo}}^{\text{homo}} = \mathbf{R}_0^{\text{rect}} \cdot \mathbf{Tr}_{\text{velo}\to\text{cam}} \cdot \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

#### 🔍 Bảng giải phẫu chi tiết từng thành phần:
| Ký hiệu | Tên gọi chuẩn | Kích thước | Đơn vị | Ý nghĩa vật lý thực tế |
| :---: | :--- | :---: | :---: | :--- |
| $\mathbf{x}_{\text{velo}}^{\text{homo}}$ | Tọa độ đồng nhất điểm LiDAR | $4 \times 1$ | mét ($\text{m}$) | Vector tọa độ $[x, y, z, 1]^T$ đo bằng cảm biến LiDAR gắn trên nóc xe. |
| $\mathbf{Tr}_{\text{velo}\to\text{cam}}$ | Ma trận ngoại suy (Extrinsic matrix) | $4 \times 4$ | - | Mô tả vị trí và góc xoay tương đối giữa cụm LiDAR và cụm Camera gốc (Camera 0). |
| $\mathbf{R}_0^{\text{rect}}$ | Ma trận nắn ảnh (Rectification matrix) | $4 \times 4$ | - | Xoay hệ tọa độ để đưa hai mắt camera stereo về cùng một mặt phẳng nằm ngang thẳng hàng. |
| $\mathbf{T}_{\text{cam}\_\text{velo}}$ | Ma trận chuyển đổi toàn phần | $4 \times 4$ | - | Tích của ma trận nắn và ma trận ngoại suy: chuyển thẳng điểm LiDAR sang camera đã nắn. |
| $\mathbf{x}_{\text{cam}}$ | Điểm trong hệ tọa độ Camera | $3 \times 1$ | mét ($\text{m}$) | Ba tọa độ không gian $[x_{\text{cam}}, y_{\text{cam}}, z_{\text{cam}}]$ theo góc nhìn của ống kính camera. |

#### 🗣️ Cách phát biểu & Diễn giải bằng lời:
> **Cách đọc:** *"Vector tọa độ điểm trong hệ camera bằng ma trận chuyển đổi toàn phần nhân với vector tọa độ đồng nhất trong hệ LiDAR."*  
> **Diễn giải trực giác:** Ta gắn cho mỗi điểm một số 1 ở đuôi (tọa độ đồng nhất), sau đó xoay và dịch chuyển toàn bộ đám mây điểm từ mốc nóc xe (LiDAR) về đúng tâm của ống kính máy ảnh (Camera). Thành phần $z_{\text{cam}}$ chính là **khoảng cách từ mặt kính máy ảnh thẳng tới vật thể**.

---

### 3.2 Giai đoạn 2: Chiếu từ không gian Camera lên mặt phẳng điểm ảnh (`cam_to_image`)

$$s \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \mathbf{P}_2 \cdot \begin{bmatrix} x_{\text{cam}} \\ y_{\text{cam}} \\ z_{\text{cam}} \\ 1 \end{bmatrix} = \begin{bmatrix} f_x & 0 & c_x & -f_x b_x \\ 0 & f_y & c_y & 0 \\ 0 & 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} x_{\text{cam}} \\ y_{\text{cam}} \\ z_{\text{cam}} \\ 1 \end{bmatrix}$$

$$\implies u = \frac{s \cdot u}{s} = \frac{f_x x_{\text{cam}} + c_x z_{\text{cam}} - f_x b_x}{z_{\text{cam}}}, \quad v = \frac{s \cdot v}{s} = \frac{f_y y_{\text{cam}} + c_y z_{\text{cam}}}{z_{\text{cam}}}$$

#### 🔍 Bảng giải phẫu chi tiết từng thành phần:
| Ký hiệu | Tên gọi chuẩn | Kích thước | Đơn vị | Ý nghĩa vật lý thực tế |
| :---: | :--- | :---: | :---: | :--- |
| $\mathbf{P}_2$ | Ma trận chiếu Camera màu bên trái | $3 \times 4$ | - | Chứa thông số nội suy quang học (tiêu cự, tâm ảnh) kết hợp với khoảng cách dịch trục giữa các camera. |
| $f_x, f_y$ | Tiêu cự theo trục ngang và trục dọc | Vô hướng | pixel | Độ phóng đại của thấu kính camera quy đổi ra đơn vị điểm ảnh. |
| $c_x, c_y$ | Điểm quang tâm (Principal point) | Vô hướng | pixel | Tọa độ giao điểm của trục quang học thấu kính với mặt phẳng cảm biến CMOS (thường gần giữa ảnh). |
| $b_x$ | Khoảng cách cơ sở (Baseline) | Vô hướng | mét ($\text{m}$) | Độ lệch vị trí giữa camera màu số 2 và camera gốc số 0 theo phương ngang. |
| $s$ | Thừa số tỷ lệ (Scale factor) | Vô hướng | mét ($\text{m}$) | Giá trị tỷ lệ tọa độ đồng nhất. Trong mô hình camera chuẩn pinhole, **$s$ chính bằng độ sâu $z_{\text{cam}}$**! |
| $u, v$ | Tọa độ điểm ảnh (Pixel coordinates) | Số thực | pixel | Vị trí hàng và cột của điểm đó trên bức ảnh hiển thị ($u$ là trục ngang, $v$ là trục dọc). |

#### 🗣️ Cách phát biểu & Diễn giải bằng lời:
> **Cách đọc:** *"Tọa độ điểm ảnh $(u, v)$ thu được bằng cách nhân ma trận chiếu $\mathbf{P}_2$ với vector vị trí trong hệ camera, sau đó lấy hai thành phần đầu chia cho thành phần thứ ba (độ sâu $z_{\text{cam}}$)."*  
> **Nguyên lý trực giác (Luật xa gần):** Vật càng ở xa ống kính ($z_{\text{cam}}$ càng lớn), khi chia cho $z_{\text{cam}}$ thì tọa độ $(u, v)$ càng co cụm lại gần tâm ảnh. Đây chính là cách máy tính mô phỏng lại hiện tượng mắt người nhìn vật ở xa thấy nhỏ đi!

---

### 3.3 Ba điều kiện lọc điểm bắt buộc trong thực tế
Dữ liệu đo đạc thực tế luôn có rác. Trước khi chiếu lên ảnh, bắt buộc phải thỏa mãn 3 điều kiện:
1. **Lọc dữ liệu hỏng:** Điểm không được chứa giá trị `NaN` (Not a Number) hoặc `Inf` (vô cực).
2. **Lọc điểm nằm sau lưng ống kính:** $z_{\text{cam}} > \text{min\_depth}$ (thường chọn $0.1\,\text{m}$). Nếu để $z_{\text{cam}} \le 0$, phép chia sẽ gây lỗi hoặc chiếu ngược các vật thể phía sau đuôi xe lên mặt kính phía trước!
3. **Lọc điểm rơi ra ngoài khung hình:** $0 \le u < W$ và $0 \le v < H$ (với $W, H$ là chiều rộng và chiều cao ảnh).

---

## 4. HƯỚNG DẪN CÀI ĐẶT 2 HÀM CỐT LÕI TRONG `starter/projection.py`

File `starter/projection.py` có sẵn khung sườn và 2 hàm `TODO(CP2)`. Học viên cần hoàn thiện chính xác bằng thư viện NumPy dạng vector (tuyệt đối không dùng vòng lặp `for` vì sẽ làm chậm hệ thống gấp hàng trăm lần).

### 4.1 Cài đặt hàm `velo_to_cam`
```python
def velo_to_cam(points_xyz: np.ndarray, calib: KittiCalib) -> np.ndarray:
    """Đưa điểm (N, 3) từ velodyne frame sang rectified camera frame (N, 3)."""
    # Bước 1: Tạo ma trận tọa độ đồng nhất (N, 4) bằng cách ghép thêm một cột toàn số 1
    N = len(points_xyz)
    points_homo = np.hstack([points_xyz, np.ones((N, 1), dtype=points_xyz.dtype)])
    
    # Bước 2: Nhân với ma trận T_cam_velo (4x4).
    # Chú ý: Dữ liệu đang có dạng hàng (N, 4), do đó công thức nhân ma trận là:
    # X_cam = X_velo @ T_cam_velo^T
    points_cam_homo = points_homo @ calib.T_cam_velo.T
    
    # Bước 3: Lấy 3 cột đầu tiên (x, y, z) trả về
    return points_cam_homo[:, :3]
```

---

### 4.2 Cài đặt hàm `cam_to_image`
```python
def cam_to_image(points_cam: np.ndarray, P2: np.ndarray, image_shape: tuple[int, ...],
                 min_depth: float = 0.1) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Chiếu điểm camera frame (N, 3) lên ảnh bằng P2 (3x4)."""
    H, W = image_shape[:2]
    N = len(points_cam)
    
    # Bước 1: Kiểm tra các giá trị hợp lệ (loại trừ NaN và Inf)
    is_finite = np.isfinite(points_cam).all(axis=1)
    z_cam = points_cam[:, 2]
    
    # Bước 2: Tạo mặt nạ ban đầu với điều kiện điểm phải nằm phía trước camera
    valid_depth = is_finite & (z_cam > min_depth)
    
    # Bước 3: Chuyển sang tọa độ đồng nhất và nhân với ma trận chiếu P2 (3x4)
    # Kết quả proj có kích thước (N, 3) ứng với [s*u, s*v, s]
    points_cam_homo = np.hstack([points_cam, np.ones((N, 1), dtype=points_cam.dtype)])
    proj = points_cam_homo @ P2.T
    
    # Khởi tạo mảng chứa tọa độ u, v
    u = np.zeros(N, dtype=np.float32)
    v = np.zeros(N, dtype=np.float32)
    
    # Bước 4: Chia cho s (chính là proj[:, 2]) đối với những điểm có độ sâu hợp lệ
    s = proj[valid_depth, 2]
    u[valid_depth] = proj[valid_depth, 0] / s
    v[valid_depth] = proj[valid_depth, 1] / s
    
    # Bước 5: Kiểm tra điểm có nằm trọn vẹn trong khung ảnh hay không
    in_bounds = valid_depth & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    mask = in_bounds
    
    uv = np.stack([u[mask], v[mask]], axis=1)
    depth = z_cam[mask]
    
    return uv, depth, mask
```

---

### 4.3 Tự kiểm tra độc lập (Sanity Check)
Chạy lệnh kiểm thử sau từ dòng lệnh:
```bash
python -m starter.projection --data-root data/synthetic --frame 000000
python -m starter.projection --data-root data/kitti_mini --frame 000011
```
- **Tiêu chuẩn đạt:** Ảnh sinh ra tại `results/figures/` hiển thị các chấm màu LiDAR bám khít lên thân xe hơi, người đi bộ, cột đèn và mặt đường; không có chấm nào bị văng lên bầu trời.
- **Kiểm tra số học thủ công:** Với frame `000000` của `data/synthetic`, điểm $(10, 0, 0)$ phải cho ra $z_{\text{cam}} \approx 9.73\,\text{m}$ và pixel $(u, v) \approx (614, 175)$ (gần chính giữa bức ảnh rộng 1242 pixel).

---

## 5. CHIẾN LƯỢC CHỌN ĐỀ TÀI ĐẠT ĐIỂM TỐI ĐA: TOPIC A (PROJECTION QA)

### 5.1 Vì sao nên chọn Topic A?
Trong 6 đề tài, **Topic A (LiDAR-camera projection QA)** là lựa chọn thông minh và an toàn nhất:
1. **Không đòi hỏi GPU NVIDIA:** Chạy mượt mà 100% trên CPU của bất kỳ máy tính nào.
2. **Khớp hoàn toàn với nội dung cốt lõi của môn học:** Đi sâu vào bản chất hình học, mô hình calibration và độ nhạy lỗi.
3. **Dễ dàng đạt trọn 10 điểm Bonus:** Có thể kết hợp so sánh thuật toán (B1), stress-test xoay góc (B2), tạo công cụ dòng lệnh hoàn chỉnh (B4), chạy trên cả KITTI lẫn nuScenes (B5), và phát hiện lỗi cài sẵn trong synthetic data (B6).

---

### 5.2 Xây dựng câu khẳng định kỹ thuật (Claim - Mục 1 REPORT)
Một claim xuất sắc phải có đủ 3 yếu tố: **đại lượng đo được**, **điều kiện cụ thể** và **ngưỡng so sánh**:

> **Câu Claim mẫu chuẩn:**  
> *"Độ lệch góc xoay Yaw $\ge 1.0^\circ$ của cảm biến LiDAR làm suy giảm hơn $15\%$ tỷ lệ điểm LiDAR rơi đúng vào hộp 2D Bounding Box của xe hơi ở khoảng cách trên $25\,\text{m}$, và hiện tượng lệch này có thể được phát hiện tự động bằng chỉ số tương thích biên cạnh (Edge Alignment Score) với ngưỡng suy giảm vượt quá $20\%$."*

---

### 5.3 Thiết kế thí nghiệm quét đa mức (CP3 Experiment Design)
Thiết kế script trong `src/eval_projection_qa.py` để quét qua ít nhất 5 mức lệch góc Yaw và 3 mức dịch chuyển:
- **Góc xoay Yaw quanh trục Z-up:** $0.0^\circ$ (chuẩn gốc), $0.5^\circ$, $1.0^\circ$, $1.5^\circ$, $2.0^\circ$, $3.0^\circ$.
- **Độ dịch chuyển tịnh tiến $t_y$ (sang trái/phải):** $0\,\text{cm}$, $5\,\text{cm}$, $10\,\text{cm}$.

#### Hai chỉ số đo đạc định lượng (Metrics):
1. **Tỷ lệ điểm nằm trong hộp vật thể (`points_in_box_ratio`):**
   Đếm số lượng điểm LiDAR đã chiếu rơi vào bên trong hộp 2D Ground Truth chia cho tổng số điểm LiDAR thuộc về vật thể đó:
   $$\text{Ratio}_{\text{box}} = \frac{\sum_{i \in \text{Object}} \mathbb{I}(u_i, v_i \in \text{BBox}_{2D})}{N_{\text{Object}}}$$
2. **Điểm tương thích biên cạnh (Edge Alignment Score - Bonus B1):**
   Dùng thuật toán Canny trên ảnh camera để tìm các đường mép vật thể (Image Edges). Đồng thời tìm các bước nhảy độ sâu (Depth Discontinuities) từ LiDAR. Tính độ trùng khớp giữa hai đường biên này.

---

## 6. PHƯƠNG PHÁP LUẬN PHÂN TÍCH LỖI QUA 6 TẦNG DEBUG HỆ THỐNG

Một trong những phần chiếm nhiều điểm nhất của bài lab (25/100 điểm) là tìm ra **Failure Case** và chỉ ra nó thuộc tầng nào trong 6 tầng kiến trúc xe tự hành:

```
┌─────────────────────────────────────────────────────────────┐
│ TẦNG 6: METRIC (Cách đo đạc & Tiêu chuẩn đánh giá)          │
├─────────────────────────────────────────────────────────────┤
│ TẦNG 5: MODEL / DETECTOR (Mô hình học sâu, ngưỡng tự tin)   │
├─────────────────────────────────────────────────────────────┤
│ TẦNG 4: PREPROCESS (Cắt cự ly range, lọc mặt đất, voxel)    │
├─────────────────────────────────────────────────────────────┤
│ TẦNG 3: TIME / SYNC (Đồng bộ thời gian & Bù chuyển động xe) │
├─────────────────────────────────────────────────────────────┤
│ TẦNG 2: GEOMETRY (Hệ trục tọa độ, Extrinsic, Projection)    │
├─────────────────────────────────────────────────────────────┤
│ TẦNG 1: I/O (Đọc file, ép kiểu dữ liệu, thứ tự kênh màu)    │
└─────────────────────────────────────────────────────────────┘
```

### 6.1 Hai ca lỗi thực tế xuất sắc để đưa vào báo cáo

#### 💥 Ca Lỗi 1: Lỗi Hình Học Cự Ly Xa (Geometry Layer Drift)
- **Tên file ảnh:** `results/figures/fail_01_yaw_2deg_distant_car.png`
- **Mô tả hiện tượng:** Khi cố tình làm lệch góc Yaw của LiDAR thêm $2.0^\circ$, với các xe ở gần ($< 10\,\text{m}$), các điểm LiDAR vẫn rơi trúng thân xe. Nhưng với chiếc xe ở khoảng cách $45\,\text{m}$, toàn bộ chùm điểm LiDAR bị trượt hẳn sang làn đường bên cạnh và văng ra ngoài hộp Bounding Box 2D!
- **Nguyên nhân toán học:** Độ lệch vị trí trên ảnh $\Delta u$ tỉ lệ thuận với cự ly thực tế:
  $$\Delta x_{\text{thực}} \approx d \cdot \sin(\Delta \theta_{\text{yaw}})$$
  Ở cự ly $d = 45\,\text{m}$ và $\Delta \theta = 2^\circ$, độ lệch không gian là:
  $$\Delta x = 45 \cdot \sin(0.0349) \approx 1.57\,\text{m}$$
  Một sai số $1.57\,\text{m}$ đủ làm chùm tia trượt hoàn toàn khỏi thân một chiếc sedan thông thường.
- **Tầng lỗi:** **Tầng 2 (Geometry Layer)**.

---

#### 💥 Ca Lỗi 2: Lỗi Bất Đồng Bộ Thời Gian Khi Xe Đang Rẽ (Time / Synchronization Layer)
- **Tên file ảnh:** `results/figures/fail_02_nuscenes_no_egomotion.png`
- **Mô tả hiện tượng:** Chạy thử trên dataset nuScenes với tùy chọn `--ignore-ego-motion`. Khi xe tự hành đang vào cua với vận tốc góc lớn, điểm LiDAR bị bóng ma (motion smear), lệch hẳn khỏi thân xe hơi đi cùng chiều.
- **Nguyên nhân gốc rễ:** Cảm biến LiDAR quay 360 độ mất $100\,\text{ms}$, trong khi camera chụp ở một thời điểm ngắt quãng lệch vài chục mili-giây. Trong khoảng thời gian lệch đó, xe tự hành đã di chuyển một đoạn $\Delta \mathbf{x} = \mathbf{v} \cdot \Delta t$ và xoay một góc $\Delta \theta = \omega \cdot \Delta t$. Nếu không bù chuyển động (Deskewing / Ego-motion compensation), phép chiếu hình học sẽ hoàn toàn sai lệch.
- **Tầng lỗi:** **Tầng 3 (Time Layer)**.

---

## 7. BÍ KÍP SĂN TRỌN 10 ĐIỂM THƯỞNG (BONUS B1 ĐẾN B6)

Bài lab cho phép cộng tối đa **+10 điểm thưởng** vào điểm tổng kết. Dưới đây là chiến lược ăn trọn 10 điểm:

| Mã Bonus | Tiêu chí | Điểm | Cách thực hiện cụ thể trong bài của bạn |
| :---: | :--- | :---: | :--- |
| **B1** | So sánh 2 thuật toán / cấu hình | **+4** | So sánh 2 cách đo độ lệch calibration: (1) Tính tỷ lệ điểm rơi trong 2D Bounding Box vs. (2) Tính điểm tương quan đường biên Canny Edge Alignment Score. |
| **B2** | Stress-test suy giảm dữ liệu | **+3** | Thử nghiệm 5 mức lệch góc Yaw ($0^\circ \to 3^\circ$) kết hợp 3 mức dịch chuyển $t_y$ ($0 \to 10\,\text{cm}$). Xuất biểu đồ trực quan. |
| **B3** | Đo tốc độ xử lý (Latency) chuẩn kỹ thuật | **+2** | Chạy lặp lại 30 lần hàm chiếu, loại bỏ lần đầu tiên (warmup), tính và báo cáo thời gian trung vị $p_{50}$ và phân vị $95$ ($p_{95}$) trên CPU. |
| **B4** | Viết công cụ dùng lại có giao diện dòng lệnh | **+3** | Tạo module `src/eval_projection_qa.py` có tham số dòng lệnh `--data-root`, `--frame`, `--yaw-deg`, `--out-dir` và `--help` đầy đủ. |
| **B5** | Chạy so sánh trên cả KITTI và nuScenes | **+2** | Chạy kiểm tra trên cả `kitti_mini` (LiDAR 64 beam) và `nuscenes_mini_subset` (LiDAR 32 beam). Chỉ ra sự khác biệt về mật độ điểm và hiệu ứng đồng bộ thời gian. |
| **B6** | Vạch trần toàn bộ lỗi trong `data/synthetic` | **+2** | Lập bảng 3 lỗi cài sẵn: (1) Điểm NaN ở mọi frame, (2) Nhảy cóc thời gian $0.2\,\text{s}$ giữa frame 2 và 3, (3) Mất chùm tia (sector dropout) ở frame 3. |

*(Tổng điểm bonus các mục trên lên tới +16 điểm, chắc chắn đạt trần tối đa +10 điểm).*

---

## 8. BÀI HỌC TRIỂN KHAI THỰC TẾ TRONG XE TỰ HÀNH & ROBOT CÔNG NGHIỆP

### 8.1 Ứng dụng thực tế: Cơ chế tự động giám sát Calibration (Online Health Monitoring)
Trong thực tế, khi xe tự hành vận hành liên tục qua hàng nghìn km:
- Ổ gà, va chạm nhẹ hoặc biến dạng nhiệt vào mùa hè khiến giá đỡ cảm biến (mounting bracket) bị biến dạng nhẹ từ $0.5^\circ$ đến $1.0^\circ$.
- Nếu không có cơ chế tự phát hiện, hệ thống nhận diện 3D sẽ bị "lác mắt", dẫn tới việc xe phanh gấp vô cớ hoặc không phát hiện chướng ngại vật phía trước.

### 8.2 Đánh đổi kỹ thuật (Engineering Trade-offs)
- **Tần số hiệu chuẩn vs. Chi phí tính toán:** Không thể chạy thuật toán tối ưu hóa calibration phức tạp ở mọi khung hình (60 FPS). Thay vào đó, hệ thống chạy một tiến trình ngầm tần số thấp ($0.5\,\text{Hz}$) để tính chỉ số Edge Alignment Score. Nếu chỉ số này sụt giảm liên tục trong 10 giây, xe sẽ phát cảnh báo yêu cầu vào trạm bảo dưỡng.
- **Độ thưa của LiDAR vs. Khoảng cách an toàn:** Với LiDAR 32 beam (như nuScenes), ở cự ly trên $40\,\text{m}$, chùm tia chỉ quét trúng một chiếc xe hơi từ 1 đến 3 điểm. Khi bị lệch calibration dù chỉ $0.5^\circ$, toàn bộ các điểm này sẽ trượt ra ngoài, khiến xe hoàn toàn tàng hình trước hệ thống phát hiện 3D!

### 8.3 Các chỉ số cần ghi log khi xe chạy thực tế
1. **Extrinsic Drift Metric:** Độ tương thích biên ảnh giữa camera và độ sâu LiDAR.
2. **LiDAR Point Cloud Density Ratio:** Số điểm hợp lệ nằm trong vùng quan tâm (ROI) của camera.
3. **Hardware Latency Jitter:** Độ chênh lệch thời gian giữa nhãn thời gian phần cứng của camera và LiDAR ($t_{\text{cam}} - t_{\text{lidar}}$).

---

## 9. CHECKLIST HOÀN THIỆN BÁO CÁO `report/REPORT.md` & NỘP BÀI

### 9.1 Kiểm tra các mục trong `report/REPORT.md`
- [ ] Thông tin học viên: Họ tên, MSSV `2A202602467`, lớp `AI20K-T4`, link repo GitHub.
- [ ] Xóa sạch toàn bộ từ khóa `[ĐIỀN]` và dấu ngoặc vuông trong toàn bộ file.
- [ ] Mục 1: Đã điền câu Claim định lượng rõ ràng.
- [ ] Mục 2: Có bảng số liệu đa mức và đường dẫn ảnh demo `../results/figures/...`.
- [ ] Mục 3: Có ảnh lỗi `fail_*.png` và giải thích rõ theo tầng lỗi hệ thống.
- [ ] Mục 4: Có khuyến nghị thực tế và đánh đổi kỹ thuật.
- [ ] Mục 5: Ghi rõ ràng các câu lệnh chạy tái lập kết quả từ đầu.
- [ ] Mục 6: Khai báo trung thực và chi tiết việc sử dụng công cụ AI hỗ trợ.

### 9.2 Lệnh kiểm tra tính hợp lệ trước khi nộp
Chạy từ thư mục gốc của repository:
```bash
python tools/check_submission.py
```
- **Kết quả đạt:** Mọi tiêu chí đều hiện `[PASS]` và dòng cuối cùng in hoa:  
  `KẾT QUẢ: SẴN SÀNG NỘP`.

### 9.3 Quy trình Commit và Đẩy lên GitHub
Tuân thủ nguyên tắc commit theo từng Checkpoint:
```bash
git add starter/projection.py src/ results/ report/REPORT.md
git commit -m "CP5: complete lab project with full benchmark, failure analysis, and report"
git push origin main
```

---
*Tài liệu hướng dẫn hoàn thành cho bài lab Day 6 / Track 4 — AI20K.*  
*Học viên: Lâm Quang Anh Quân (MSSV: `2A202602467`).*
