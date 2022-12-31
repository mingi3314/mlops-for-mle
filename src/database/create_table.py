import sqlalchemy as sa
from sqlalchemy.engine.base import Engine

from src.config import DB_URL


def create_table(engine: Engine) -> None:
    # Create a connection to the database
    with engine.connect() as conn:
        # Create a table
        conn.execute(
            "CREATE TABLE IF NOT EXISTS iris_data (id serial PRIMARY KEY, sepal_length float,"
            " sepal_width float, petal_length float, petal_width float, target int)"
        )


if __name__ == "__main__":
    # Create a database engine
    engine = sa.create_engine(DB_URL, echo=True)
    create_table(engine)
