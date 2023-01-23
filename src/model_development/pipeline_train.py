from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from src.model_development.base_train import load_data, preprocess


def pipeline_train(host: str = None, verbose: bool = False) -> Pipeline:
    X_train, X_test, y_train, y_test = preprocess(load_data(host))

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", SVC()),
        ]
    )

    pipeline.fit(X_train, y_train)

    if verbose:
        print(f"train accuracy: {pipeline.score(X_train, y_train)}")
        print(f"test accuracy: {pipeline.score(X_test, y_test)}")

    return pipeline


if __name__ == "__main__":
    pipeline_train()
