import os

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.database.engine import create_engine


def load_data(host: str = None) -> pd.DataFrame:
    enigne = create_engine(host)
    df = pd.read_sql("SELECT * from iris_data ORDER BY id DESC LIMIT 100;", enigne)
    return df


def preprocess(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = df.drop("target", axis=1)
    y = df["target"]

    # Split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def train(scaled_X_train: pd.DataFrame, y_train: pd.Series) -> SVC:
    model = SVC()
    model.fit(scaled_X_train, y_train)

    y_train_hat = model.predict(scaled_X_train)

    print("Train accuracy:", accuracy_score(y_train, y_train_hat))
    return model


def test(scaled_X_test: pd.DataFrame, y_test: pd.Series, model: SVC) -> None:
    y_test_hat = model.predict(scaled_X_test)

    print("Test accuracy:", accuracy_score(y_test, y_test_hat))


def save_model(model: SVC, scaler: StandardScaler, directory: str) -> None:
    os.makedirs(directory, exist_ok=True)
    joblib.dump(model, f"{directory}/model.pkl")
    joblib.dump(scaler, f"{directory}/scaler.pkl")


def load_model(directory: str) -> tuple[SVC, StandardScaler]:
    model = joblib.load(f"{directory}/model.pkl")
    scaler = joblib.load(f"{directory}/scaler.pkl")
    return model, scaler


def main() -> None:
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess(df)

    model_dir = "src/model_development/models"
    if os.path.exists("models/model.pkl"):
        model, scaler = load_model(model_dir)
    else:
        scaler = StandardScaler()
        scaled_X_train = scaler.fit_transform(X_train)
        model = train(scaled_X_train, y_train)
        save_model(model, scaler, model_dir)

    scaled_X_test = scaler.transform(X_test)
    test(scaled_X_test, y_test, model)


if __name__ == "__main__":
    main()
