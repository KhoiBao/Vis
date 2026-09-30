import os


class Settings:

    APP_NAME = "2D Geometry Lab API"

    APP_VERSION = "1.0.0"

    NEO4J_URI = os.getenv(
        "NEO4J_URI",
        "bolt://localhost:7687"
    )

    NEO4J_USERNAME = os.getenv(
        "NEO4J_USERNAME",
        "neo4j"
    )

    NEO4J_PASSWORD = os.getenv(
        "NEO4J_PASSWORD",
        "password"
    )


settings = Settings()