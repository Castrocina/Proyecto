import pytest
from evaluarModelos import cargarModelosyDatos
import numpy as np
from sklearn.metrics import precision_score
X_train,y_train,X_val,y_val,X_test,y_test,modeloRLog,modeloXGBoost,x_preprocess_pipeline,y_preprocess_pipeline,preprocesado_path = cargarModelosyDatos()
#total_pred = np.append(np.append(y_test,y_val),y_train)


def test_accuracy_higher_than_benchmark():
    
    # The following lines are for calculating the benchmark, the benchmark accuracy should be updated with the best model accuracy once is live in production
    #unique, counts = np.unique(total_pred, return_counts=True)
    #print(dict(zip(unique, counts)))

    # Initial Benchmark
    benchmark_predictions = [0] * len(y_test)
    benchmark_accuracy = precision_score(y_test, benchmark_predictions, average='weighted', zero_division=0)
    
    # Getting the accuracy of the model
    predictions_rlog = modeloRLog.predict(X_test)
    actual_accuracy_rlog = precision_score(y_test, predictions_rlog, average='weighted', zero_division=0)
    
    print(f'Accuracy of model rlog: {actual_accuracy_rlog}, Accuracy of Benchmark: {benchmark_accuracy}')

    predictions_XGBoost = modeloXGBoost.predict(X_test)
    actual_accuracy_XGBoost = precision_score(y_test, predictions_XGBoost, average='weighted', zero_division=0)
    
    print(f'Accuracy of model XGBOOST: {actual_accuracy_XGBoost}, Accuracy of Benchmark: {benchmark_accuracy}')
    
    # Comparing the accuracy of the first model against the benchmark
    assert actual_accuracy_rlog > benchmark_accuracy
    assert actual_accuracy_XGBoost > benchmark_accuracy

