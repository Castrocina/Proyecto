import mlflow


def get_artifacts(mlflow_url,mlflow_exp_name,mlflow_run_name,model_path):
    mlflow.set_tracking_uri(mlflow_url)
    print(mlflow_run_name)
    run_id = mlflow.search_runs(search_all_experiments=True,filter_string=f"run_name='{mlflow_run_name}'")['run_id'].values[0]
    modelo_full_path = f'mlflow-artifacts:/1/{run_id}/artifacts/{model_path}' 
    pipelineX_full_path = f'mlflow-artifacts:/1/{run_id}/artifacts/X_preprocess_pipeline' 
    pipeliney_full_path = f'mlflow-artifacts:/1/{run_id}/artifacts/y_preprocess_pipeline' 
    

    modelo = mlflow.sklearn.load_model(modelo_full_path)
    pipelineX = mlflow.sklearn.load_model(pipelineX_full_path)
    pipeliney = mlflow.sklearn.load_model(pipeliney_full_path)

    return modelo, pipelineX, pipeliney