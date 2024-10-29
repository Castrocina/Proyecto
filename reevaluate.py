import mlflow
import sys
import pandas as pd
sys.path.insert(0, './refactoring')
import evaluarModelos

mlflow.set_tracking_uri("http://127.0.0.1:5000")

run_name = sys.argv[1]

experiment_name = "Cirrhosis V1"

run_id = mlflow.search_runs(search_all_experiments=True,filter_string=f"run_name='{run_name}'")['run_id'].values[0]

logreg_model_path  = f'mlflow-artifacts:/1/{run_id}/artifacts/LogRegresion_model'
XGBoost_model_path =  f'mlflow-artifacts:/1/{run_id}/artifacts/XGBoost_model'

logreg_model=mlflow.sklearn.load_model(logreg_model_path)
XGBoost_model=mlflow.sklearn.load_model(XGBoost_model_path)


run = mlflow.get_run(run_id)

dataset_source = mlflow.data.get_source(run.inputs.dataset_inputs[0])
dataset_loaded = dataset_source.load()

for dataset_input in run.inputs.dataset_inputs:
    dataset_context = dataset_input.tags[0]._value
    dataset_source = mlflow.data.get_source(dataset_input)
    dataset_path = dataset_source.load()

    match dataset_context:
        case "input train":
            X_train=pd.read_csv(dataset_path)
        case "target train":
             y_train=pd.read_csv(dataset_path)
        case "input val":
             X_val=pd.read_csv(dataset_path)
        case "target val":
             y_val=pd.read_csv(dataset_path)
        case "input test":
             X_test=pd.read_csv(dataset_path)
        case "target test":
             y_test=pd.read_csv(dataset_path)

evaluar_logreg = evaluarModelos.evaluarModelo(logreg_model,X_train,y_train,X_val,y_val,X_test,y_test,"regresion logistica",False)
evaluar_logreg.evaluar()
evaluar_XGBoost = evaluarModelos.evaluarModelo(XGBoost_model,X_train,y_train,X_val,y_val,X_test,y_test,"XGBoost",False)
evaluar_XGBoost.evaluar()
