import os

import click
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score

from src.model_development.base_train import load_data, preprocess

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"


@click.command()
@click.option("--run-id", help="Run ID", type=click.STRING)
@click.option("--model-name", help="Name of the model", type=click.STRING)
def main(run_id: str, model_name: str) -> None:
    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(f"runs:/{run_id}/{model_name}")

    # Predict on a Pandas DataFrame.

    X_train, X_test, y_train, y_test = preprocess(load_data())

    pred_train = loaded_model.predict(pd.DataFrame(X_train))
    pred_test = loaded_model.predict(pd.DataFrame(X_test))

    print("Train accuracy:", accuracy_score(y_train, pred_train))
    print("Test accuracy:", accuracy_score(y_test, pred_test))


if __name__ == "__main__":
    main()
