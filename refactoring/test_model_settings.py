import pytest
from evaluarModelos import cargarModelosyDatos
import numpy as np

X_train,y_train,X_val,y_val,X_test,y_test,modeloRLog,modeloXGBoost,x_preprocess_pipeline,y_preprocess_pipeline,preprocesado_path = cargarModelosyDatos()

def test_rlog_settings():
    model_params = modeloRLog.get_params()
    expected_params = {'C': 0.3, 'class_weight': 'balanced', 'dual': False, 'fit_intercept': True, 'intercept_scaling': 1, 'l1_ratio': 0, 'max_iter': 5000, 'multi_class': 'auto', 'n_jobs': None, 'penalty': 'elasticnet', 'random_state': None, 'solver': 'saga', 'tol': 0.0001, 'verbose': 0, 'warm_start': False}

    assert model_params==expected_params

def test_XGBOOST_settings():
    model_params = modeloXGBoost.get_params()
    del model_params["missing"]
    expected_params =  {'objective': 'multi:softprob', 'base_score': None, 'booster': None, 'callbacks': None, 'colsample_bylevel': None, 'colsample_bynode': None, 'colsample_bytree': 0.6, 'device': None, 'early_stopping_rounds': None, 'enable_categorical': False, 'eval_metric': 'logloss', 'feature_types': None, 'gamma': None, 'grow_policy': None, 'importance_type': None, 'interaction_constraints': None, 'learning_rate': 0.05, 'max_bin': None, 'max_cat_threshold': None, 'max_cat_to_onehot': None, 'max_delta_step': None, 'max_depth': 2, 'max_leaves': None, 'min_child_weight': 1, 'monotone_constraints': None, 'multi_strategy': None, 'n_estimators': 200, 'n_jobs': None, 'num_parallel_tree': None, 'random_state': None, 'reg_alpha': None, 'reg_lambda': None, 'sampling_method': None, 'scale_pos_weight': None, 'subsample': 1, 'tree_method': None, 'validate_parameters': None, 'verbosity': None, 'use_label_encoder': 'False', 'alpha': 0, 'lambda': 1}
    
    assert model_params==expected_params