# Geometry Specification

> **Project:** Phòng Thí Nghiệm Hình Học 2D
> **Module:** Mô hình hóa & Suy luận Hình học phẳng với Neo4j
> **Version:** 1.0
> **Status:** Chốt cho MVP

---

## 1. Mục đích

Tài liệu này định nghĩa thống nhất các quy ước, dữ liệu đầu vào, công thức hình học, phép kiểm tra quan hệ và luật phân loại tứ giác được sử dụng trong hệ thống.

Mục tiêu là đảm bảo:

* Frontend và Backend sử dụng cùng một quy ước hình học.
* Geometry Engine là nguồn tính toán hình học duy nhất.
* Neo4j lưu trữ được các đối tượng và quan hệ hình học.
* Các luật suy luận trong Cypher sử dụng các fact đã được Geometry Engine xác định.
* Kết quả phân loại giữa Frontend, Backend và Neo4j không mâu thuẫn.
* Có thể kiểm thử các trường hợp hình học một cách nhất quán.

---

# 2. Phạm vi MVP

Hệ thống xử lý **tứ giác ABCD trên mặt phẳng tọa độ 2D**.

MVP hỗ trợ:

### Đối tượng

* Điểm `A, B, C, D`.
* Cạnh `AB, BC, CD, DA`.
* Đường chéo `AC, BD`.
* Tứ giác `ABCD`.

### Thuộc tính hình học

* Độ dài cạnh.
* Độ dài đường chéo.
* Chu vi.
* Diện tích.
* Góc tại A, B, C, D.
* Cạnh song song.
* Cạnh vuông góc.
* Cạnh bằng nhau.
* Đường chéo.
* Tính lồi/lõm.
* Tính hợp lệ của tứ giác.

### Phân loại

* Tứ giác thường.
* Hình thang.
* Hình thang cân.
* Hình thang vuông.
* Hình bình hành.
* Hình chữ nhật.
* Hình thoi.
* Hình vuông.

---

# 3. Mô hình hình học

## 3.1. Thứ tự đỉnh

Các đỉnh phải được cung cấp theo thứ tự quanh biên tứ giác:

```text
A → B → C → D → A
```

Do đó các cạnh là:

```text
AB
BC
CD
DA
```

và hai đường chéo:

```text
AC
BD
```

Không chấp nhận việc nhập đỉnh theo thứ tự ngẫu nhiên.

---

# 4. Hệ tọa độ

Mỗi điểm được biểu diễn bởi:

```json
{
  "x": 0,
  "y": 0
}
```

Ví dụ:

```json
{
  "A": { "x": 0, "y": 0 },
  "B": { "x": 4, "y": 0 },
  "C": { "x": 4, "y": 3 },
  "D": { "x": 0, "y": 3 }
}
```

Đơn vị tọa độ được xem là **đơn vị hình học**, không phụ thuộc pixel của Canvas.

Frontend chỉ chuyển đổi:

```text
tọa độ hình học ↔ tọa độ màn hình
```

Backend chỉ xử lý tọa độ hình học.

---

# 5. Độ dài đoạn thẳng

Với:

```text
P(x₁, y₁)
Q(x₂, y₂)
```

độ dài:

```text
|PQ| = √((x₂ - x₁)² + (y₂ - y₁)²)
```

Áp dụng:

```text
AB = distance(A, B)
BC = distance(B, C)
CD = distance(C, D)
DA = distance(D, A)

AC = distance(A, C)
BD = distance(B, D)
```

---

# 6. Vector

Vector từ P đến Q:

```text
PQ = (xQ - xP, yQ - yP)
```

Các vector cạnh:

```text
AB = B - A
BC = C - B
CD = D - C
DA = A - D
```

Lưu ý:

`DA` được hiểu là vector từ D đến A.

---

# 7. Tích vô hướng

Với:

```text
u = (ux, uy)
v = (vx, vy)
```

tích vô hướng:

```text
u · v = ux × vx + uy × vy
```

Dùng để kiểm tra vuông góc.

Hai vector vuông góc khi:

```text
|u · v| <= EPSILON
```

---

# 8. Tích có hướng 2D

Với:

```text
u = (ux, uy)
v = (vx, vy)
```

cross product:

```text
cross(u, v) = ux × vy - uy × vx
```

Dùng để:

* xác định hướng quay.
* kiểm tra thẳng hàng.
* kiểm tra tính lồi.
* hỗ trợ kiểm tra giao nhau của đoạn thẳng.

---

# 9. EPSILON

Không được sử dụng phép so sánh trực tiếp:

```python
a == b
```

cho các giá trị hình học thực.

Sử dụng:

```python
```
