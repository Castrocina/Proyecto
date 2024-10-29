import mlflow
import sys



mlflow.set_tracking_uri("http://127.0.0.1:5000")

run_name = sys.argv[1]

experiment_name = "Cirrhosis V1"

run_id = mlflow.search_runs(search_all_experiments=True,filter_string=f"run_name='{run_name}'")['run_id'].values[0]

#logreg_model_path  = f'mlflow-artifacts:/1/{run_id}/artifacts/LogRegresion_model'
#XGBoost_model_path =  f'mlflow-artifacts:/1/{run_id}/artifacts/XGBoost_model'

#logreg_model=mlflow.sklearn.load_model(logreg_model_path)
#XGBoost_model=mlflow.sklearn.load_model(XGBoost_model_path)

#X_test =  mlflow.data.get_source()
#y_test_path = 


run = mlflow.get_run(run_id)

dataset_source = mlflow.data.get_source(run.inputs.dataset_inputs[0])
#dataset_source.load()

print(run.inputs.dataset_inputs[0].dataset)
