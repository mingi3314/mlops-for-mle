import os

import click
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.model_development.base_train import load_data, preprocess

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"


@click.command()
@click.option("--model-name", default="iris_svc", help="Name of the model", type=click.STRING)
def main(model_name: str) -> None:
    X_train, X_test, y_train, y_test = preprocess(load_data())

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", SVC()),
        ]
    )

    pipeline.fit(X_train, y_train)

    signature = infer_signature(X_train, pipeline.predict(X_train))
    input_example = X_train.iloc[:5, :]

    mlflow.set_experiment("new-experiment")

    with mlflow.start_run():
        mlflow.log_metric("train_accuracy", pipeline.score(X_train, y_train))
        mlflow.log_metric("test_accuracy", pipeline.score(X_test, y_test))
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path=model_name,
            signature=signature,
            input_example=input_example,
        )


if __name__ == "__main__":
    main()
