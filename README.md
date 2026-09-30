# 🧮 Ứng dụng Mô hình hóa & Suy luận Hình học phẳng (Tứ giác 2D) với Neo4j

## 1. Tổng quan

Dự án xây dựng một ứng dụng Web cho phép người dùng **mô hình hóa, phân tích và phân loại tứ giác 2D** dựa trên tọa độ các đỉnh.

Hệ thống sử dụng:

* **Frontend Canvas** để vẽ và tương tác với tứ giác.
* **Python/FastAPI** làm Backend và xử lý nghiệp vụ.
* **Geometry Engine** để thực hiện các phép tính hình học.
* **Neo4j** để mô hình hóa các đối tượng và quan hệ hình học dưới dạng Graph.
* **Cypher Query** để thực thi các quy tắc suy luận và phân loại tứ giác.
* **Swagger/OpenAPI** để kiểm thử và tài liệu hóa API.

### Mục tiêu chính

```text
Vẽ tứ giác
    ↓
Lấy tọa độ các đỉnh
    ↓
Tính toán các thuộc tính hình học
    ↓
Mô hình hóa dữ liệu thành Graph
    ↓
Lưu vào Neo4j
    ↓
Áp dụng các quy tắc suy luận
    ↓
Phân loại tứ giác
    ↓
Hiển thị kết quả + Graph + thông tin hình học
```

---

# 2. Phạm vi dự án

## 2.1. Chức năng chính

Hệ thống cần hỗ trợ:

* Tạo tứ giác ABCD từ 4 điểm.
* Kéo/thả các đỉnh trên Canvas.
* Tính độ dài các cạnh.
* Tính độ dài hai đường chéo.
* Tính chu vi.
* Tính diện tích.
* Tính góc.
* Xác định hai đoạn thẳng có song song hay không.
* Xác định hai đoạn thẳng có vuông góc hay không.
* Kiểm tra các cạnh có bằng nhau hay không.
* Kiểm tra tứ giác hợp lệ.
* Mô hình hóa tứ giác trong Neo4j.
* Lưu các quan hệ hình học.
* Suy luận loại tứ giác bằng các quy tắc được định nghĩa.
* Hiển thị kết quả phân loại.
* Hiển thị Graph tương ứng trong Neo4j.

## 2.2. Các loại tứ giác dự kiến

Hệ thống hỗ trợ nhận diện:

* Tứ giác
* Hình thang
* Hình thang cân
* Hình thang vuông
* Hình bình hành
* Hình chữ nhật
* Hình thoi
* Hình vuông

### Lưu ý

Việc phân loại không nên xem các loại trên là hoàn toàn loại trừ nhau.

Ví dụ:

```text
Hình vuông
├── Hình chữ nhật
├── Hình thoi
├── Hình bình hành
└── Tứ giác
```

Vì vậy hệ thống có thể hiển thị:

```text
Loại chính:
    Hình vuông

Các tính chất thỏa mãn:
    ✓ Hình chữ nhật
    ✓ Hình thoi
    ✓ Hình bình hành
    ✓ Tứ giác
```

---

# 3. Kiến trúc hệ thống

```text
┌──────────────────────────────────────────────────┐
│                    FRONTEND                      │
│                                                  │
│  HTML5 Canvas + JavaScript                      │
│  - Vẽ tứ giác                                   │
│  - Kéo thả điểm                                 │
│  - Hiển thị kết quả                             │
│  - Hiển thị Graph                               │
└──────────────────────┬───────────────────────────┘
                       │ REST API
                       ▼
┌──────────────────────────────────────────────────┐
│                    BACKEND                       │
│                                                  │
│                  FastAPI                         │
│                                                  │
│  ┌────────────────┐   ┌──────────────────────┐  │
│  │ Geometry Engine│   │  Neo4j Integration   │  │
│  │                │   │                      │  │
│  │ - Distance     │   │ - Create Graph       │  │
│  │ - Angle        │   │ - Query Graph        │  │
│  │ - Parallel     │   │ - Store Relations    │  │
│  │ - Perpendicular│   │ - Cypher Rules       │  │
│  │ - Area         │   │                      │  │
│  │ - Perimeter    │   └──────────┬───────────┘  │
│  └───────┬────────┘              │              │
│          │                       │              │
└──────────┼───────────────────────┼──────────────┘
           │                       │
           │                       ▼
           │              ┌──────────────────┐
           │              │      Neo4j       │
           │              │                  │
           │              │ Graph Database   │
           │              │                  │
           │              │ Nodes + Relations│
           │              └──────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────┐
│                  RESULT                          │
│                                                  │
│  - Geometric properties                         │
│  - Quadrilateral classification                 │
│  - Derived relationships                        │
│  - Graph representation                         │
└──────────────────────────────────────────────────┘
```

---

# 4. Công nghệ

| Thành phần      | Công nghệ                    |
| --------------- | ---------------------------- |
| Frontend        | HTML5, CSS3, JavaScript ES6+ |
| Drawing         | HTML5 Canvas                 |
| Backend         | Python                       |
| API Framework   | FastAPI                      |
| Validation      | Pydantic                     |
| Geometry        | Python `math` / NumPy        |
| Database        | Neo4j                        |
| Query           | Cypher                       |
| Database Driver | Neo4j Python Driver          |
| API Testing     | Swagger / OpenAPI            |
| Version Control | Git                          |
| Container       | Docker / Docker Compose      |

> React/Vue/Tailwind chỉ sử dụng nếu cần thiết. Không đưa thêm framework nếu Canvas + JavaScript đã đáp ứng được yêu cầu.

---

# 5. Mô hình dữ liệu hình học

## 5.1. Point

```text
Point
- id
- name
- x
- y
```

Ví dụ:

```text
A(100, 100)
B(400, 100)
C(400, 300)
D(100, 300)
```

## 5.2. Segment

```text
Segment
- id
- name
- length
```

Ví dụ:

```text
AB
BC
CD
DA
AC
BD
```

## 5.3. Quadrilateral

```text
Quadrilateral
- id
- name
- area
- perimeter
- classification
```

---

# 6. Neo4j Graph Schema

Mô hình cơ bản:

```text
(:Quadrilateral)-[:HAS_VERTEX]->(:Point)

(:Quadrilateral)-[:HAS_EDGE]->(:Segment)

(:Quadrilateral)-[:HAS_DIAGONAL]->(:Segment)
```

Quan hệ hình học:

```text
(:Segment)-[:PARALLEL_TO]->(:Segment)

(:Segment)-[:PERPENDICULAR_TO]->(:Segment)

(:Segment)-[:INTERSECTS_AT]->(:Point)

(:Point)-[:MIDPOINT_OF]->(:Segment)

(:Segment)-[:DIAGONAL_OF]->(:Quadrilateral)
```

Ví dụ:

```text
AB ── PARALLEL_TO ── CD

AD ── PARALLEL_TO ── BC

AB ── PERPENDICULAR_TO ── BC
```

---

# 7. Geometry Engine

Geometry Engine chịu trách nhiệm biến tọa độ thành các **facts hình học**.

## 7.1. Tính toán

Phải hỗ trợ tối thiểu:

* Khoảng cách giữa hai điểm.
* Độ dài đoạn thẳng.
* Độ dài đường chéo.
* Chu vi.
* Diện tích.
* Góc giữa hai đoạn/vector.

## 7.2. Quan hệ hình học

Phải xác định:

```text
AB ∥ CD
AB ⟂ BC
AB = CD
AB = BC
```

## 7.3. Kiểm tra hình hợp lệ

Kiểm tra:

* Không có hai đỉnh trùng nhau.
* Không có cạnh có độ dài bằng 0.
* Tứ giác không tự giao nhau.
* Các điểm không suy biến.
* Có thể kiểm tra tứ giác lồi nếu phạm vi dự án yêu cầu.

## 7.4. Floating-point tolerance

Không so sánh số thực bằng `==`.

Ví dụ:

```python
abs(a - b) < EPSILON
```

Tương tự với:

* Hai độ dài bằng nhau.
* Hai vector vuông góc.
* Hai vector song song.

Giá trị `EPSILON` phải được thống nhất trong toàn bộ Backend.

---

# 8. Bộ quy tắc suy luận

Các quy tắc được định nghĩa trước và thực thi thông qua Cypher.

## 8.1. Hình bình hành

```text
AB ∥ CD
AND
AD ∥ BC

→ Parallelogram
```

## 8.2. Hình chữ nhật

```text
Parallelogram
AND
AB ⟂ BC

→ Rectangle
```

## 8.3. Hình thoi

```text
Parallelogram
AND
AB = BC

→ Rhombus
```

## 8.4. Hình vuông

```text
Rectangle
AND
AB = BC

→ Square
```

## 8.5. Hình thang

Quy ước về "hình thang" phải được thống nhất trong nhóm.

Nếu sử dụng định nghĩa "có ít nhất một cặp cạnh đối song song":

```text
AB ∥ CD
OR
AD ∥ BC

→ Trapezoid
```

Nếu sử dụng định nghĩa "chỉ có một cặp cạnh đối song song", điều kiện phải được điều chỉnh tương ứng.

**Quy ước cuối cùng phải được ghi rõ trong tài liệu dự án.**

---

# 9. API

Backend cung cấp REST API.

## Phân tích tứ giác

```http
POST /api/quadrilaterals/analyze
```

Input:

```json
{
  "A": {"x": 100, "y": 100},
  "B": {"x": 400, "y": 100},
  "C": {"x": 400, "y": 300},
  "D": {"x": 100, "y": 300}
}
```

Output dự kiến:

```json
{
  "vertices": {},
  "edges": {},
  "diagonals": {},
  "angles": {},
  "area": 60000,
  "perimeter": 1000,
  "relations": [
    "AB_PARALLEL_CD",
    "AD_PARALLEL_BC",
    "AB_PERPENDICULAR_BC"
  ],
  "classification": [
    "Quadrilateral",
    "Parallelogram",
    "Rectangle"
  ]
}
```

Các endpoint khác có thể bổ sung:

```text
POST /api/quadrilaterals
POST /api/quadrilaterals/analyze
POST /api/quadrilaterals/classify
GET  /api/quadrilaterals/{id}
GET  /api/quadrilaterals/{id}/graph
```

Tất cả API phải được kiểm thử thông qua **Swagger/OpenAPI**.

---

# 10. Phân công thành viên

| Thành viên | Vai trò                  | Trách nhiệm                                                       |
| ---------- | ------------------------ | ----------------------------------------------------------------- |
| **Dev 1**  | Neo4j & Inference        | Graph Schema, Nodes, Relationships, Cypher, Rules, Classification |
| **Dev 2**  | Backend & Geometry       | FastAPI, Pydantic, Geometry Engine, API, Neo4j Driver             |
| **Dev 3**  | Frontend & Visualization | Canvas, Drag & Drop, UI, API Client, Graph Visualization          |

## Trách nhiệm chung

Cả 3 thành viên cùng tham gia:

* Thiết kế kiến trúc.
* Thống nhất API contract.
* Kiểm thử tích hợp.
* Debug lỗi liên module.
* Chuẩn bị demo.
* Viết tài liệu và báo cáo.

Không nên để mỗi thành viên chỉ hiểu phần của mình.

---

# 11. Quy định hoàn thành

Một chức năng chỉ được xem là hoàn thành khi:

* Code đã chạy được.
* Có test hoặc test thủ công rõ ràng.
* Không phá vỡ chức năng hiện có.
* API được kiểm thử bằng Swagger nếu liên quan Backend.
* Code đã được push lên Git.
* Có README/documentation cần thiết.
* Ít nhất một thành viên khác đã review.

---

# 12. Tiêu chí Demo chính

Demo tối thiểu phải thực hiện được flow:

```text
1. Người dùng mở ứng dụng
          ↓
2. Tạo tứ giác ABCD
          ↓
3. Kéo các điểm để thay đổi hình
          ↓
4. Gửi dữ liệu lên Backend
          ↓
5. Geometry Engine tính toán
          ↓
6. Dữ liệu được lưu vào Neo4j
          ↓
7. Cypher thực thi các quy tắc
          ↓
8. Hệ thống xác định loại tứ giác
          ↓
9. Hiển thị kết quả
          ↓
10. Hiển thị Graph tương ứng
```

---

# 13. Ví dụ kết quả mong muốn

Với hình chữ nhật:

```text
AB ∥ CD
AD ∥ BC

AB ⟂ BC

AB = CD
AD = BC

Area = AB × AD
Perimeter = 2 × (AB + AD)

⇒ Hình bình hành
⇒ Hình chữ nhật
```

Với hình vuông:

```text
AB ∥ CD
AD ∥ BC

AB ⟂ BC

AB = BC
BC = CD
CD = DA

⇒ Hình bình hành
⇒ Hình chữ nhật
⇒ Hình thoi
⇒ Hình vuông
```

---

# 14. Hướng phát triển

Các chức năng sau **không thuộc MVP bắt buộc**, chỉ thực hiện nếu còn thời gian:

### Natural Language Geometry

Cho phép người dùng nhập:

> "Cho tứ giác ABCD có AB song song CD..."

Sau đó hệ thống phân tích thành các facts:

```text
AB ∥ CD
```

và đưa vào Graph.

### Proof / Reasoning Trace

Hiển thị chuỗi suy luận:

```text
AB ∥ CD
AD ∥ BC
       ↓
Hình bình hành
       ↓
AB ⟂ BC
       ↓
Hình chữ nhật
```

### Advanced Visualization

* Highlight cạnh song song.
* Highlight góc vuông.
* Hiển thị đường chéo.
* Click vào node Graph để highlight đối tượng trên Canvas.

---

# 15. Nguyên tắc thiết kế quan trọng

### 1. Neo4j không phải Geometry Engine

Neo4j chịu trách nhiệm:

```text
Lưu trữ + biểu diễn quan hệ + truy vấn + suy luận dựa trên rule
```

Geometry Engine chịu trách nhiệm:

```text
Tính toán hình học từ tọa độ
```

### 2. Cypher không phải bộ giải hình học tổng quát

Cypher dùng để kiểm tra các facts và áp dụng những quy tắc đã được nhóm định nghĩa.

Không tuyên bố rằng:

> "Neo4j tự động hiểu và giải bài hình học."

Cách mô tả chính xác:

> "Hệ thống sử dụng Neo4j để biểu diễn các đối tượng và quan hệ hình học dưới dạng đồ thị. Các quy tắc hình học được định nghĩa bằng Cypher được sử dụng để suy luận các thuộc tính và phân loại tứ giác."

### 3. Ưu tiên MVP

MVP phải tập trung vào:

```text
Canvas
  +
Geometry Engine
  +
FastAPI
  +
Neo4j
  +
Cypher Classification
```

Không mở rộng sang NLP hoặc AI nếu các thành phần cốt lõi chưa ổn định.

---

# 16. Repository Structure

Cấu trúc đề xuất:

```text
project-root/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── geometry/
│   │   │   ├── neo4j/
│   │   │   └── inference/
│   │   └── core/
│   │
│   ├── tests/
│   └── requirements.txt
│
├── neo4j/
│   ├── schema/
│   └── queries/
│
├── docs/
│   ├── architecture.md
│   ├── graph-schema.md
│   └── inference-rules.md
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# 17. Git Workflow

Branch chính:

```text
main
```

Branch phát triển:

```text
develop
```

Feature branch:

```text
feature/frontend-canvas
feature/geometry-engine
feature/neo4j-schema
feature/inference-rules
feature/api
```

Quy trình:

```text
feature/*
    ↓
Pull Request
    ↓
Code Review
    ↓
develop
    ↓
main
```

Commit nên mô tả rõ thay đổi:

```text
feat: add quadrilateral geometry calculation
feat: add neo4j graph schema
feat: implement rectangle inference rule
fix: handle self-intersecting quadrilateral
```

---

# 18. Mục tiêu cuối cùng

Sau khi hoàn thành, hệ thống phải thể hiện được rõ 4 thành phần cốt lõi:

```text
             GEOMETRY
                 │
                 ▼
          ┌─────────────┐
          │  Tứ giác 2D │
          └──────┬──────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
 Geometry Engine        Neo4j Graph
       │                   │
       │              Relationships
       │                   │
       └─────────┬─────────┘
                 ▼
          Inference Rules
                 │
                 ▼
        Quadrilateral Type
                 │
                 ▼
        Visualization/UI
```

**Giá trị chính của đề tài không nằm ở việc "vẽ được tứ giác", mà nằm ở việc kết hợp mô hình hình học với Graph Database để biểu diễn quan hệ và thực hiện suy luận dựa trên các quy tắc hình học.**
