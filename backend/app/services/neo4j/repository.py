from neo4j import GraphDatabase

from app.core.config import settings


class Neo4jRepository:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(
                settings.NEO4J_USERNAME,
                settings.NEO4J_PASSWORD
            )
        )

    def close(self):
        self.driver.close()

    def verify_connection(self):
        self.driver.verify_connectivity()

    def save_quadrilateral(
        self,
        quadrilateral_id: str,
        facts: dict
    ):

        query = """
        MERGE (q:Quadrilateral {id: $id})

        SET q.area = $area,
            q.perimeter = $perimeter,
            q.convex = $convex

        WITH q

        MERGE (a:Point {
            quadrilateralId: $id,
            name: 'A'
        })

        SET a.x = $ax,
            a.y = $ay

        MERGE (b:Point {
            quadrilateralId: $id,
            name: 'B'
        })

        SET b.x = $bx,
            b.y = $by

        MERGE (c:Point {
            quadrilateralId: $id,
            name: 'C'
        })

        SET c.x = $cx,
            c.y = $cy

        MERGE (d:Point {
            quadrilateralId: $id,
            name: 'D'
        })

        SET d.x = $dx,
            d.y = $dy

        MERGE (q)-[:HAS_VERTEX]->(a)
        MERGE (q)-[:HAS_VERTEX]->(b)
        MERGE (q)-[:HAS_VERTEX]->(c)
        MERGE (q)-[:HAS_VERTEX]->(d)

        RETURN q
        """

        vertices = facts["vertices"]

        parameters = {
            "id": quadrilateral_id,

            "area": facts["area"],
            "perimeter": facts["perimeter"],
            "convex": facts["convex"],

            "ax": vertices["A"]["x"],
            "ay": vertices["A"]["y"],

            "bx": vertices["B"]["x"],
            "by": vertices["B"]["y"],

            "cx": vertices["C"]["x"],
            "cy": vertices["C"]["y"],

            "dx": vertices["D"]["x"],
            "dy": vertices["D"]["y"],
        }

        with self.driver.session() as session:
            result = session.run(
                query,
                parameters
            )

            record = result.single()

        self.save_segments(
            quadrilateral_id,
            facts
        )

        return record

    # =========================================================
    # SEGMENTS + GEOMETRY RELATIONS
    #
    # CypherInference tra về kết quả chỉ khi graph có:
    #   (:Quadrilateral)-[:HAS_EDGE]->(:Segment)
    #   (:Segment)-[:PARALLEL_TO]->(:Segment)
    #   (:Segment)-[:PERPENDICULAR_TO]->(:Segment)
    #   (:Segment)-[:EQUAL_TO]->(:Segment)
    # =========================================================

    # =========================================================
    # READ
    # =========================================================

    def get_quadrilateral(
        self,
        quadrilateral_id: str
    ) -> dict | None:

        query = """
        MATCH (q:Quadrilateral {id: $id})

        OPTIONAL MATCH (q)-[:HAS_VERTEX]->(p:Point)
        WITH q, collect(p { .name, .x, .y }) AS vertices

        OPTIONAL MATCH (q)-[:HAS_EDGE]->(e:Segment)
        WITH q, vertices, collect(e { .name, .length }) AS edges

        OPTIONAL MATCH (q)-[:HAS_DIAGONAL]->(d:Segment)
        WITH q, vertices, edges, collect(d { .name, .length }) AS diagonals

        RETURN q {
            .id,
            .area,
            .perimeter,
            .convex,
            .classification,
            .classifications
        } AS properties,
        vertices,
        edges,
        diagonals
        """

        with self.driver.session() as session:
            record = session.run(
                query,
                {"id": quadrilateral_id}
            ).single()

        if record is None:
            return None

        return {
            **record["properties"],
            "vertices": record["vertices"],
            "edges": record["edges"],
            "diagonals": record["diagonals"],
        }

    def get_graph(
        self,
        quadrilateral_id: str
    ) -> dict | None:

        query = """
        MATCH (q:Quadrilateral {id: $id})

        OPTIONAL MATCH (q)-[:HAS_VERTEX|HAS_EDGE|HAS_DIAGONAL]->(n)
        WITH q, collect(DISTINCT n) AS linked

        OPTIONAL MATCH (a)-[r:PARALLEL_TO|PERPENDICULAR_TO|EQUAL_TO]->(b)
        WHERE a IN linked AND b IN linked

        WITH q,
             linked,
             collect(DISTINCT {
                 type: type(r),
                 from: a.name,
                 to: b.name
             }) AS relationships

        RETURN [x IN ([q] + linked) WHERE x IS NOT NULL | {
            label: head(labels(x)),
            name: coalesce(x.name, 'Quadrilateral'),
            x: x.x,
            y: x.y,
            length: x.length
        }] AS nodes,
        [rel IN relationships WHERE rel.type IS NOT NULL] AS relationships
        """

        with self.driver.session() as session:
            record = session.run(
                query,
                {"id": quadrilateral_id}
            ).single()

        if record is None:
            return None

        return {
            "id": quadrilateral_id,
            "nodes": record["nodes"],
            "relationships": record["relationships"],
        }

    # =========================================================

    def save_segments(
        self,
        quadrilateral_id: str,
        facts: dict
    ):

        query = """
        MATCH (q:Quadrilateral {id: $id})

        MERGE (ab:Segment {quadrilateralId: $id, name: 'AB'})
        SET ab.length = $ab_length

        MERGE (bc:Segment {quadrilateralId: $id, name: 'BC'})
        SET bc.length = $bc_length

        MERGE (cd:Segment {quadrilateralId: $id, name: 'CD'})
        SET cd.length = $cd_length

        MERGE (da:Segment {quadrilateralId: $id, name: 'DA'})
        SET da.length = $da_length

        MERGE (ac:Segment {quadrilateralId: $id, name: 'AC'})
        SET ac.length = $ac_length

        MERGE (bd:Segment {quadrilateralId: $id, name: 'BD'})
        SET bd.length = $bd_length

        MERGE (q)-[:HAS_EDGE]->(ab)
        MERGE (q)-[:HAS_EDGE]->(bc)
        MERGE (q)-[:HAS_EDGE]->(cd)
        MERGE (q)-[:HAS_EDGE]->(da)

        MERGE (q)-[:HAS_DIAGONAL]->(ac)
        MERGE (q)-[:HAS_DIAGONAL]->(bd)

        WITH ab, bc, cd, da, ac, bd

        FOREACH (_ IN CASE WHEN $parallel_ab_cd THEN [1] ELSE [] END |
            MERGE (ab)-[:PARALLEL_TO]->(cd)
        )

        FOREACH (_ IN CASE WHEN $parallel_bc_da THEN [1] ELSE [] END |
            MERGE (bc)-[:PARALLEL_TO]->(da)
        )

        FOREACH (_ IN CASE WHEN $perpendicular_ab_bc THEN [1] ELSE [] END |
            MERGE (ab)-[:PERPENDICULAR_TO]->(bc)
        )

        FOREACH (_ IN CASE WHEN $perpendicular_bc_cd THEN [1] ELSE [] END |
            MERGE (bc)-[:PERPENDICULAR_TO]->(cd)
        )

        FOREACH (_ IN CASE WHEN $perpendicular_cd_da THEN [1] ELSE [] END |
            MERGE (cd)-[:PERPENDICULAR_TO]->(da)
        )

        FOREACH (_ IN CASE WHEN $perpendicular_da_ab THEN [1] ELSE [] END |
            MERGE (da)-[:PERPENDICULAR_TO]->(ab)
        )

        FOREACH (_ IN CASE WHEN $equal_ab_bc THEN [1] ELSE [] END |
            MERGE (ab)-[:EQUAL_TO]->(bc)
        )

        FOREACH (_ IN CASE WHEN $equal_bc_cd THEN [1] ELSE [] END |
            MERGE (bc)-[:EQUAL_TO]->(cd)
        )

        FOREACH (_ IN CASE WHEN $equal_cd_da THEN [1] ELSE [] END |
            MERGE (cd)-[:EQUAL_TO]->(da)
        )

        FOREACH (_ IN CASE WHEN $equal_da_ab THEN [1] ELSE [] END |
            MERGE (da)-[:EQUAL_TO]->(ab)
        )

        FOREACH (_ IN CASE WHEN $equal_ab_cd THEN [1] ELSE [] END |
            MERGE (ab)-[:EQUAL_TO]->(cd)
        )

        FOREACH (_ IN CASE WHEN $equal_bc_da THEN [1] ELSE [] END |
            MERGE (bc)-[:EQUAL_TO]->(da)
        )

        FOREACH (_ IN CASE WHEN $equal_ac_bd THEN [1] ELSE [] END |
            MERGE (ac)-[:EQUAL_TO]->(bd)
        )

        RETURN ab
        """

        edges = facts["edges"]
        diagonals = facts["diagonals"]

        parallel = facts["relations"]["parallel"]
        perpendicular = facts["relations"]["perpendicular"]
        equal = facts["relations"]["equal"]

        parameters = {
            "id": quadrilateral_id,

            "ab_length": edges["AB"],
            "bc_length": edges["BC"],
            "cd_length": edges["CD"],
            "da_length": edges["DA"],

            "ac_length": diagonals["AC"],
            "bd_length": diagonals["BD"],

            "parallel_ab_cd": parallel["AB_CD"],
            "parallel_bc_da": parallel["BC_DA"],

            "perpendicular_ab_bc": perpendicular["AB_BC"],
            "perpendicular_bc_cd": perpendicular["BC_CD"],
            "perpendicular_cd_da": perpendicular["CD_DA"],
            "perpendicular_da_ab": perpendicular["DA_AB"],

            "equal_ab_bc": equal["AB_BC"],
            "equal_bc_cd": equal["BC_CD"],
            "equal_cd_da": equal["CD_DA"],
            "equal_da_ab": equal["DA_AB"],

            "equal_ab_cd": equal["AB_CD"],
            "equal_bc_da": equal["BC_DA"],

            "equal_ac_bd": equal["AC_BD"],
        }

        with self.driver.session() as session:
            result = session.run(
                query,
                parameters
            )

            return result.single()