import time

import click

from src.database.create_table import create_table
from src.database.engine import create_engine
from src.database.insert_data import fetch_data, insert_data


@click.option("--db-host", default="localhost", help="Database host")
@click.command()
def main(db_host: str) -> None:
    engine = create_engine(db_host)
    create_table(engine)

    df_iris = fetch_data()

    for data in df_iris.to_dicts():
        insert_data(engine, data)
        time.sleep(1)


if __name__ == "__main__":
    main()
