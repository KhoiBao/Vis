from pydantic import BaseModel


class Point(BaseModel):
    x: float
    y: float


class QuadrilateralRequest(BaseModel):
    A: Point
    B: Point
    C: Point
    D: Point