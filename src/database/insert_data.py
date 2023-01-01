from typing import Any

import polars as pl
import sqlalchemy as sa
from sklearn.datasets import load_iris
from sqlalchemy.engine.base import Engine


def fetch_data() -> pl.DataFrame:
    df_iris = pl.from_pandas(load_iris(as_frame=True)["frame"])
    df_iris.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "target"]
    return df_iris


def insert_data(engine: Engine, data: dict[str, Any]) -> None:

    query = sa.text(
        "INSERT INTO iris_data (sepal_length, sepal_width, petal_length, petal_width, target)"
        " VALUES (:sepal_length, :sepal_width, :petal_length, :petal_width, :target)"
    )

    with engine.connect() as conn:
        conn.execute(query, **data)


if __name__ == "__main__":
    from src.database.engine import create_engine

    df_iris = fetch_data()

    insert_data(create_engine(), df_iris.to_dicts()[0])
