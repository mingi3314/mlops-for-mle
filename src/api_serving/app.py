import mlflow
from fastapi import FastAPI
from mlflow.pyfunc import PyFuncModel
from src.api_serving.schema import PredictIn, PredictOut


def get_model() -> PyFuncModel:
    model = mlflow.pyfunc.load_model("src/api_serving/iris_svc")
    return model


app = FastAPI()
model = get_model()


@app.post("/predict", response_model=PredictOut)
async def predict(input_data: PredictIn) -> PredictOut:
    prediction = model.predict([input_data.dict()])
    return PredictOut(iris_class=prediction[0])
