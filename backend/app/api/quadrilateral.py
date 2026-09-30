from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas.geometry import QuadrilateralRequest

from app.services.geometry.engine import (
    analyze_quadrilateral,
)

from app.services.inference.classifier import (
    classify as python_classify,
)

from app.services.neo4j.repository import (
    Neo4jRepository,
)

from app.services.inference.cypher_inference import (
    CypherInference,
)


router = APIRouter(
    prefix="/api/quadrilaterals",
    tags=["Quadrilateral"]
)


# =========================================================
# ANALYZE ONLY
# Không cần Neo4j
# =========================================================

@router.post("/analyze")
def analyze(data: QuadrilateralRequest):

    facts = analyze_quadrilateral(data)

    if not facts["valid"]:
        raise HTTPException(
            status_code=400,
            detail=facts["error"]
        )

    classification = python_classify(facts)

    return {
        **facts,
        "classification": classification
    }


# =========================================================
# CREATE + SAVE + CYPHER INFERENCE
# =========================================================

@router.post("")
def create(data: QuadrilateralRequest):

    facts = analyze_quadrilateral(data)

    if not facts["valid"]:
        raise HTTPException(
            status_code=400,
            detail=facts["error"]
        )

    quadrilateral_id = str(uuid4())

    repository = Neo4jRepository()

    try:

        repository.verify_connection()

        repository.save_quadrilateral(
            quadrilateral_id,
            facts
        )

        inference = CypherInference(repository)

        classification = inference.classify(
            quadrilateral_id
        )

        return {
            "id": quadrilateral_id,
            **facts,
            "classification": classification
        }

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Neo4j error: {exc}"
        )

    finally:
        repository.close()


# =========================================================
# CLASSIFY EXISTING GRAPH
# =========================================================

@router.post("/{quadrilateral_id}/classify")
def classify(quadrilateral_id: str):

    repository = Neo4jRepository()

    try:

        repository.verify_connection()

        data = repository.get_quadrilateral(
            quadrilateral_id
        )

        if data is None:
            raise HTTPException(
                status_code=404,
                detail="Quadrilateral not found"
            )

        inference = CypherInference(repository)

        classification = inference.classify(
            quadrilateral_id
        )

        return {
            "id": quadrilateral_id,
            "classification": classification
        }

    finally:
        repository.close()


# =========================================================
# GET QUADRILATERAL
# =========================================================

@router.get("/{quadrilateral_id}")
def get_quadrilateral(
    quadrilateral_id: str
):

    repository = Neo4jRepository()

    try:

        repository.verify_connection()

        result = repository.get_quadrilateral(
            quadrilateral_id
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Quadrilateral not found"
            )

        return result

    finally:
        repository.close()


# =========================================================
# GET GRAPH
# =========================================================

@router.get("/{quadrilateral_id}/graph")
def get_graph(
    quadrilateral_id: str
):

    repository = Neo4jRepository()

    try:

        repository.verify_connection()

        graph = repository.get_graph(
            quadrilateral_id
        )

        if graph is None:
            raise HTTPException(
                status_code=404,
                detail="Graph not found"
            )

        return graph

    finally:
        repository.close()