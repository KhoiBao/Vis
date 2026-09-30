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

            return result.single()