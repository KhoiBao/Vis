from app.services.geometry.calculations import (
    cross,
    dot,
)

EPSILON = 1e-9


def is_parallel(u, v) -> bool:
    return abs(cross(u, v)) <= EPSILON


def is_perpendicular(u, v) -> bool:
    return abs(dot(u, v)) <= EPSILON


def is_equal_length(a: float, b: float) -> bool:
    return abs(a - b) <= EPSILON