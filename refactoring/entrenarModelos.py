from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pickle
import sys
import pandas as pd
from loadParams import load_params

def entrenar_modelo(model,param_grid,X_train,y_train):
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train.ravel())

        return grid_search.best_estimator_

def modeloRlog(X_train,y_train):
        modelo_logistico = LogisticRegression(max_iter=5000)
        param_grid_logistico = [
                {
                        'penalty': ['l1', 'l2'],
                        'C': [0.01, 0.1, 1, 10],
                        'solver': ['saga'],
                },
                {
                       'penalty': ['elasticnet'],
                        'C': [0.01, 0.1, 1, 10],
                        'solver': ['saga'],
                        'l1_ratio': [0, 0.5, 1]  # Sólo para elasticnet 
                }
        ]
        
        modelo = modelo_logistico
        modelo = entrenar_modelo(modelo,param_grid_logistico,X_train,y_train)
        return modelo


def modeloXGboost(X_train,y_train):
        modelo_xgboost = XGBClassifier(use_label_encoder=True, eval_metric='logloss')
        param_grid_xgboost = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'use_label_encoder':["False"]
    }
        modelo = modelo_xgboost
        modelo = entrenar_modelo(modelo,param_grid_xgboost,X_train,y_train)
        return modelo

def salvarModelo(modelo,path):
        print(path)
        pickle.dump(modelo, open(path, 'wb'))

if __name__ == '__main__':
        parametros = load_params()
        preprocesado_path = parametros["data"]["preprocesdePath"]
        modelos_path = parametros["modelos"]["path"]

        X_train = pd.read_csv(preprocesado_path+"X_train.csv")
        y_train = pd.read_csv(preprocesado_path+"y_train.csv").values.ravel()

        modeloLogRegresion = modeloRlog(X_train,y_train)
        modeloXG = modeloXGboost(X_train,y_train)

        salvarModelo(modeloLogRegresion,modelos_path+"modeloRegLog.sav")
        salvarModelo(modeloXG,modelos_path+"modeloXGBoost.sav")
        
        