from app.schemas.geometry import (
    Point,
    QuadrilateralRequest,
)

from app.services.geometry.engine import (
    analyze_quadrilateral,
)

from app.services.inference.classifier import (
    classify,
)


def test_rectangle():

    data = QuadrilateralRequest(
        A=Point(x=0, y=0),
        B=Point(x=4, y=0),
        C=Point(x=4, y=3),
        D=Point(x=0, y=3),
    )

    result = analyze_quadrilateral(data)

    assert result["valid"] is True

    assert result["area"] == 12

    assert result["perimeter"] == 14

    assert result["edges"]["AB"] == 4

    assert result["edges"]["BC"] == 3

    assert result["diagonals"]["AC"] == 5

    classifications = classify(result)

    assert "Quadrilateral" in classifications

    assert "Parallelogram" in classifications

    assert "Rectangle" in classifications


def test_square():

    data = QuadrilateralRequest(
        A=Point(x=0, y=0),
        B=Point(x=4, y=0),
        C=Point(x=4, y=4),
        D=Point(x=0, y=4),
    )

    result = analyze_quadrilateral(data)

    classifications = classify(result)

    assert "Square" in classifications

    assert "Rectangle" in classifications

    assert "Rhombus" in classifications

    assert "Parallelogram" in classifications