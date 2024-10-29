import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

run_id = "66260eb5964d48af9ed8d458ee34483d"

logged_model = f'mlflow-artifacts:/1/{run_id}/artifacts/LogRegresion_model'

# Load model as a sklearn model.
loaded_model = mlflow.sklearn.load_model(logged_model)

print(loaded_model)