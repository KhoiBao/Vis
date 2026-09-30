import math

from app.schemas.geometry import Point


EPSILON = 1e-9


def distance(p1: Point, p2: Point) -> float:
    return math.hypot(
        p2.x - p1.x,
        p2.y - p1.y
    )


def vector(p1: Point, p2: Point) -> tuple[float, float]:
    return (
        p2.x - p1.x,
        p2.y - p1.y
    )


def dot(u: tuple[float, float], v: tuple[float, float]) -> float:
    return u[0] * v[0] + u[1] * v[1]


def cross(u: tuple[float, float], v: tuple[float, float]) -> float:
    return u[0] * v[1] - u[1] * v[0]


def angle_between(
    u: tuple[float, float],
    v: tuple[float, float]
) -> float:

    length_u = math.hypot(*u)
    length_v = math.hypot(*v)

    if length_u <= EPSILON or length_v <= EPSILON:
        raise ValueError("Cannot calculate angle of zero-length vector.")

    cosine = dot(u, v) / (length_u * length_v)

    # Tránh lỗi floating point như 1.0000000002
    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(math.acos(cosine))


def polygon_area(points: list[Point]) -> float:
    area = 0.0
    n = len(points)

    for i in range(n):
        j = (i + 1) % n

        area += (
            points[i].x * points[j].y
            - points[j].x * points[i].y
        )

    return abs(area) / 2.0