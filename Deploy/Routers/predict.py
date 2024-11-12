from fastapi import APIRouter
import os
import sys
from dotenv import load_dotenv
import pandas as pd
import json 

sys.path.insert(0, '../')
from get_artifacts import get_artifacts
from cirrhosis_model_class import PredictionRequest


dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)  # take environment variables from .env.


mlflow_url =  os.getenv("MLFLOW_URL")
mlflow_exp_name = os.getenv("MLFLOW_EXP_NAME")
mlflow_run_name = os.getenv("MLFLOW_RUN_NAME")
model_path = os.getenv("MODEL_PATH")


modelo, pipelineX, pipeliney = get_artifacts(mlflow_url,mlflow_exp_name,mlflow_run_name,model_path)


router = APIRouter(
    prefix="/predict",
    tags=["predictions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def predict(data:PredictionRequest):
    json_data = data.model_dump()
    data_dict = json_data["data"]
    for dataKey in data_dict:
        data_dict[dataKey]=[data_dict[dataKey]]
    cirrhosis_data_df = pd.DataFrame.from_dict(data_dict)
    preprocesed_data = pipelineX.transform(cirrhosis_data_df)
    predictions = modelo.predict(preprocesed_data)
    target_name_mapping = dict(zip(pipeliney.transform(pipeliney.classes_),pipeliney.classes_))
    mapped_prediciton = target_name_mapping[predictions[0]]
    return {"prediction": mapped_prediciton, "prediction_name": "Status"} 