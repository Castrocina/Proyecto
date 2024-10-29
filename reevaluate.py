import mlflow
import sys



mlflow.set_tracking_uri("http://127.0.0.1:5000")

run_name = sys.argv[0]

mlflow.search_runs(filter_string="run_name='my_run'")['run_id']

logged_model = f'mlflow-artifacts:/1/{run_id}/artifacts/LogRegresion_model'

# Load model as a sklearn model.
loaded_model = mlflow.sklearn.load_model(logged_model)

print(loaded_model)