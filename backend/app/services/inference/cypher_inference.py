from app.services.neo4j.repository import Neo4jRepository


class CypherInference:

    def __init__(self, repository: Neo4jRepository):
        self.repository = repository

    def classify(
        self,
        quadrilateral_id: str
    ) -> list[str]:

        result = ["Quadrilateral"]

        with self.repository.driver.session() as session:

            if self._is_trapezoid(
                session,
                quadrilateral_id
            ):
                result.append("Trapezoid")

            if self._is_isosceles_trapezoid(
                session,
                quadrilateral_id
            ):
                result.append("Isosceles Trapezoid")

            if self._is_right_trapezoid(
                session,
                quadrilateral_id
            ):
                result.append("Right Trapezoid")

            if self._is_parallelogram(
                session,
                quadrilateral_id
            ):
                result.append("Parallelogram")

            if self._is_rectangle(
                session,
                quadrilateral_id
            ):
                result.append("Rectangle")

            if self._is_rhombus(
                session,
                quadrilateral_id
            ):
                result.append("Rhombus")

            if self._is_square(
                session,
                quadrilateral_id
            ):
                result.append("Square")

        self._save_classification(
            quadrilateral_id,
            result
        )

        return result

    # =========================================================

    def _exists(
        self,
        session,
        query: str,
        quadrilateral_id: str
    ) -> bool:

        record = session.run(
            query,
            {"id": quadrilateral_id}
        ).single()

        return (
            record is not None
            and record["matched"] is True
        )

    # =========================================================
    # TRAPEZOID
    # At least one opposite pair parallel.
    # =========================================================

    def _is_trapezoid(self, session, qid):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            (
                EXISTS {
                    MATCH (ab)-[:PARALLEL_TO]-(cd)
                }
                OR
                EXISTS {
                    MATCH (bc)-[:PARALLEL_TO]-(da)
                }
            ) AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================
    # PARALLELOGRAM
    # =========================================================

    def _is_parallelogram(self, session, qid):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            EXISTS {
                MATCH (ab)-[:PARALLEL_TO]-(cd)
            }
            AND
            EXISTS {
                MATCH (bc)-[:PARALLEL_TO]-(da)
            }
            AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================
    # RECTANGLE
    # =========================================================

    def _is_rectangle(self, session, qid):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            EXISTS {
                MATCH (ab)-[:PARALLEL_TO]-(cd)
            }
            AND
            EXISTS {
                MATCH (bc)-[:PARALLEL_TO]-(da)
            }
            AND
            EXISTS {
                MATCH (ab)-[:PERPENDICULAR_TO]-(bc)
            }
            AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================
    # RHOMBUS
    # =========================================================

    def _is_rhombus(self, session, qid):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            EXISTS {
                MATCH (ab)-[:PARALLEL_TO]-(cd)
            }
            AND
            EXISTS {
                MATCH (bc)-[:PARALLEL_TO]-(da)
            }
            AND
            EXISTS {
                MATCH (ab)-[:EQUAL_TO]-(bc)
            }
            AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================
    # SQUARE
    # =========================================================

    def _is_square(self, session, qid):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            EXISTS {
                MATCH (ab)-[:PARALLEL_TO]-(cd)
            }
            AND
            EXISTS {
                MATCH (bc)-[:PARALLEL_TO]-(da)
            }
            AND
            EXISTS {
                MATCH (ab)-[:PERPENDICULAR_TO]-(bc)
            }
            AND
            EXISTS {
                MATCH (ab)-[:EQUAL_TO]-(bc)
            }
            AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================
    # ISOSCELES TRAPEZOID
    # =========================================================

    def _is_isosceles_trapezoid(
        self,
        session,
        qid
    ):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            (
                EXISTS {
                    MATCH (ab)-[:PARALLEL_TO]-(cd)
                }
                AND
                EXISTS {
                    MATCH (bc)-[:EQUAL_TO]-(da)
                }
            )
            OR
            (
                EXISTS {
                    MATCH (bc)-[:PARALLEL_TO]-(da)
                }
                AND
                EXISTS {
                    MATCH (ab)-[:EQUAL_TO]-(cd)
                }
            )
            AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================
    # RIGHT TRAPEZOID
    # =========================================================

    def _is_right_trapezoid(
        self,
        session,
        qid
    ):

        query = """
        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(ab:Segment {name:'AB'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(bc:Segment {name:'BC'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(cd:Segment {name:'CD'})

        MATCH (:Quadrilateral {id: $id})
              -[:HAS_EDGE]->(da:Segment {name:'DA'})

        RETURN
            (
                EXISTS {
                    MATCH (ab)-[:PARALLEL_TO]-(cd)
                }
                OR
                EXISTS {
                    MATCH (bc)-[:PARALLEL_TO]-(da)
                }
            )
            AND
            (
                EXISTS {
                    MATCH (ab)-[:PERPENDICULAR_TO]-(bc)
                }
                OR
                EXISTS {
                    MATCH (bc)-[:PERPENDICULAR_TO]-(cd)
                }
                OR
                EXISTS {
                    MATCH (cd)-[:PERPENDICULAR_TO]-(da)
                }
                OR
                EXISTS {
                    MATCH (da)-[:PERPENDICULAR_TO]-(ab)
                }
            )
            AS matched
        """

        return self._exists(session, query, qid)

    # =========================================================

    def _save_classification(
        self,
        quadrilateral_id: str,
        classifications: list[str]
    ):

        query = """
        MATCH (q:Quadrilateral {id: $id})

        SET q.classifications = $classifications,
            q.classification = $primary
        """

        primary = (
            classifications[-1]
            if classifications
            else "Quadrilateral"
        )

        with self.repository.driver.session() as session:
            session.run(
                query,
                {
                    "id": quadrilateral_id,
                    "classifications": classifications,
                    "primary": primary,
                }
            ).consume()