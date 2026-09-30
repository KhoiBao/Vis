from app.schemas.geometry import QuadrilateralRequest

from app.services.geometry.calculations import (
    angle_between,
    distance,
    polygon_area,
    vector,
)

from app.services.geometry.relations import (
    is_equal_length,
    is_parallel,
    is_perpendicular,
)

from app.services.geometry.validation import (
    validate_quadrilateral,
)


def analyze_quadrilateral(q: QuadrilateralRequest) -> dict:

    A = q.A
    B = q.B
    C = q.C
    D = q.D

    validation = validate_quadrilateral(A, B, C, D)

    if not validation["valid"]:
        return {
            "valid": False,
            "error": validation["reason"]
        }

    # ==========================
    # Length
    # ==========================

    AB = distance(A, B)
    BC = distance(B, C)
    CD = distance(C, D)
    DA = distance(D, A)

    AC = distance(A, C)
    BD = distance(B, D)

    # ==========================
    # Vector
    # ==========================

    vAB = vector(A, B)
    vBC = vector(B, C)
    vCD = vector(C, D)
    vDA = vector(D, A)

    # ==========================
    # Area / perimeter
    # ==========================

    perimeter = AB + BC + CD + DA

    area = polygon_area([
        A,
        B,
        C,
        D
    ])

    # ==========================
    # Angles
    # ==========================

    angle_A = angle_between(
        vector(A, D),
        vector(A, B)
    )

    angle_B = angle_between(
        vector(B, A),
        vector(B, C)
    )

    angle_C = angle_between(
        vector(C, B),
        vector(C, D)
    )

    angle_D = angle_between(
        vector(D, C),
        vector(D, A)
    )

    # ==========================
    # Relations
    # ==========================

    relations = {

        "parallel": {
            "AB_CD": is_parallel(vAB, vCD),
            "BC_DA": is_parallel(vBC, vDA),
        },

        "perpendicular": {
            "AB_BC": is_perpendicular(vAB, vBC),
            "BC_CD": is_perpendicular(vBC, vCD),
            "CD_DA": is_perpendicular(vCD, vDA),
            "DA_AB": is_perpendicular(vDA, vAB),
        },

        "equal": {
            "AB_BC": is_equal_length(AB, BC),
            "BC_CD": is_equal_length(BC, CD),
            "CD_DA": is_equal_length(CD, DA),
            "DA_AB": is_equal_length(DA, AB),

            "AB_CD": is_equal_length(AB, CD),
            "BC_DA": is_equal_length(BC, DA),

            "AC_BD": is_equal_length(AC, BD),
        }
    }

    return {

        "valid": True,

        "convex": validation["convex"],

        "vertices": {
            "A": A.model_dump(),
            "B": B.model_dump(),
            "C": C.model_dump(),
            "D": D.model_dump(),
        },

        "edges": {
            "AB": AB,
            "BC": BC,
            "CD": CD,
            "DA": DA,
        },

        "diagonals": {
            "AC": AC,
            "BD": BD,
        },

        "angles": {
            "A": angle_A,
            "B": angle_B,
            "C": angle_C,
            "D": angle_D,
        },

        "area": area,

        "perimeter": perimeter,

        "relations": relations,
    }