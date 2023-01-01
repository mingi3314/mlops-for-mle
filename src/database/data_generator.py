import time

from src.database.create_table import create_table
from src.database.engine import create_engine
from src.database.insert_data import fetch_data, insert_data

if __name__ == "__main__":
    create_table(engine=create_engine())

    df_iris = fetch_data()

    for data in df_iris.to_dicts():
        insert_data(create_engine(), data)
        time.sleep(1)
