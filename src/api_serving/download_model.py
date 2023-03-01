import os

import click
import mlflow

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"


@click.command()
@click.option("--run-id", required=True, help="Run ID", type=click.STRING)
@click.option("--model-name", required=True, help="Name of the model", type=click.STRING)
@click.option("--dst-path", help="Destination path", type=click.STRING, default=".")
def download_model(run_id: str, model_name: str, dst_path: str) -> None:
    mlflow.artifacts.download_artifacts(
        artifact_uri=f"runs:/{run_id}/{model_name}", dst_path=dst_path
    )


if __name__ == "__main__":
    download_model()
