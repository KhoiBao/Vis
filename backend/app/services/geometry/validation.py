from app.schemas.geometry import Point

from app.services.geometry.calculations import (
    cross,
    distance,
    vector,
)


EPSILON = 1e-9


def same_point(p1: Point, p2: Point) -> bool:
    return distance(p1, p2) <= EPSILON


def orientation(a: Point, b: Point, c: Point) -> float:
    ab = vector(a, b)
    ac = vector(a, c)

    return cross(ab, ac)


def on_segment(a: Point, b: Point, p: Point) -> bool:
    return (
        min(a.x, b.x) - EPSILON <= p.x <= max(a.x, b.x) + EPSILON
        and
        min(a.y, b.y) - EPSILON <= p.y <= max(a.y, b.y) + EPSILON
    )


def segments_intersect(
    a: Point,
    b: Point,
    c: Point,
    d: Point
) -> bool:

    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    # Giao nhau thông thường
    if (
        ((o1 > EPSILON and o2 < -EPSILON) or
         (o1 < -EPSILON and o2 > EPSILON))
        and
        ((o3 > EPSILON and o4 < -EPSILON) or
         (o3 < -EPSILON and o4 > EPSILON))
    ):
        return True

    # Trường hợp thẳng hàng
    if abs(o1) <= EPSILON and on_segment(a, b, c):
        return True

    if abs(o2) <= EPSILON and on_segment(a, b, d):
        return True

    if abs(o3) <= EPSILON and on_segment(c, d, a):
        return True

    if abs(o4) <= EPSILON and on_segment(c, d, b):
        return True

    return False


def is_convex(points: list[Point]) -> bool:
    signs = []

    for i in range(4):
        a = points[i]
        b = points[(i + 1) % 4]
        c = points[(i + 2) % 4]

        value = orientation(a, b, c)

        if abs(value) > EPSILON:
            signs.append(value > 0)

    if not signs:
        return False

    return all(sign == signs[0] for sign in signs)


def validate_quadrilateral(
    A: Point,
    B: Point,
    C: Point,
    D: Point
) -> dict:

    points = [A, B, C, D]

    # 1. Không cho phép hai điểm trùng nhau
    for i in range(4):
        for j in range(i + 1, 4):
            if same_point(points[i], points[j]):
                return {
                    "valid": False,
                    "reason": "Two or more vertices overlap."
                }

    # 2. Không có cạnh bằng 0
    edges = [
        (A, B),
        (B, C),
        (C, D),
        (D, A),
    ]

    for start, end in edges:
        if distance(start, end) <= EPSILON:
            return {
                "valid": False,
                "reason": "Quadrilateral contains zero-length edge."
            }

    # 3. Kiểm tra tự giao nhau
    if segments_intersect(A, B, C, D):
        return {
            "valid": False,
            "reason": "Edges AB and CD intersect."
        }

    if segments_intersect(B, C, D, A):
        return {
            "valid": False,
            "reason": "Edges BC and DA intersect."
        }

    return {
        "valid": True,
        "reason": None,
        "convex": is_convex(points)
    }