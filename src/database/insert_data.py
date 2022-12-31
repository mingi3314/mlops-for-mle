import polars as pl
import sqlalchemy as sa
from sklearn.datasets import load_iris
from sqlalchemy.engine.base import Engine


def insert_data(engine: Engine) -> None:
    df_iris = pl.from_pandas(load_iris(as_frame=True)["frame"])
    df_iris.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "target"]

    query = sa.text(
        "INSERT INTO iris_data (sepal_length, sepal_width, petal_length, petal_width, target)"
        " VALUES (:sepal_length, :sepal_width, :petal_length, :petal_width, :target)"
    )

    with engine.connect() as conn:
        conn.execute(query, **df_iris.to_dicts()[0])


if __name__ == "__main__":
    from src.database.engine import engine

    insert_data(engine)
