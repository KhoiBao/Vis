def classify(facts: dict) -> list[str]:

    result = ["Quadrilateral"]

    relations = facts["relations"]

    parallel = relations["parallel"]
    perpendicular = relations["perpendicular"]
    equal = relations["equal"]

    opposite_parallel = (
        parallel["AB_CD"]
        and parallel["BC_DA"]
    )

    one_parallel_pair = (
        parallel["AB_CD"]
        or parallel["BC_DA"]
    )

    all_sides_equal = (
        equal["AB_BC"]
        and equal["BC_CD"]
        and equal["CD_DA"]
    )

    has_right_angle = (
        perpendicular["AB_BC"]
        or perpendicular["BC_CD"]
        or perpendicular["CD_DA"]
        or perpendicular["DA_AB"]
    )

    # Trapezoid:
    # sử dụng định nghĩa "ít nhất một cặp cạnh đối song song"
    if one_parallel_pair:
        result.append("Trapezoid")

    if opposite_parallel:
        result.append("Parallelogram")

    if opposite_parallel and has_right_angle:
        result.append("Rectangle")

    if opposite_parallel and all_sides_equal:
        result.append("Rhombus")

    if (
        opposite_parallel
        and has_right_angle
        and all_sides_equal
    ):
        result.append("Square")

    return result