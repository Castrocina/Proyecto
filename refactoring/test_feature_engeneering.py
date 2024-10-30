import pytest
from preprocess import preprocess,load_data
import numpy as np
import pandas as pd

X_test,y_test,X_val,y_val,X_train,y_train,parametros = load_data()
X_test_preprocesed,y_test_preprocesed,X_val_preprocesed,y_val_preprocesed,X_train_preprocesed,y_train_preprocesed,x_preprocess_pipeline,y_preprocess_pipeline = preprocess(X_test,y_test,X_val,y_val,X_train,y_train)
original_numeric = X_test.select_dtypes(include=np.number).drop(["Stage"],axis=1)
preprocesed_df = pd.DataFrame(X_train_preprocesed,columns=x_preprocess_pipeline.get_feature_names_out())

def test_scaler_preprocessing_brings_x_train_mean_near_zero():
    original_mean = original_numeric.mean()
    preprocesed_mean = preprocesed_df[original_numeric.columns].mean()
    assert (original_mean > preprocesed_mean).all()
    print(f'The mean of the original X train is: {original_mean}')
    print(f'The mean of the transformed X train is: {preprocesed_mean}')
    assert np.isclose(preprocesed_mean, 0.0, atol=1e-3).all()


def test_scaler_preprocessing_brings_x_train_std_near_one():
    preprocesed_std = preprocesed_df[original_numeric.columns].std()
    assert np.isclose(preprocesed_std, 1.0, atol=1e-2).all()
    print(f'The SD of the transformed X train is : {preprocesed_std}')
    


