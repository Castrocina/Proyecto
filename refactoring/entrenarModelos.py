from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pickle
import sys
import pandas as pd

def entrenar_modelo(model,param_grid,X_train,y_train):
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        return grid_search.best_estimator_

def modeloRlog(X_train,y_train):
        modelo_logistico = LogisticRegression(max_iter=5000)
        param_grid_logistico = {
            'penalty': ['l1', 'l2', 'elasticnet'],
            'C': [0.01, 0.1, 1, 10],
            'solver': ['saga'],
            'l1_ratio': [0, 0.5, 1]  # Sólo para elasticnet
        }
        modelo = modelo_logistico
        modelo = entrenar_modelo(modelo,param_grid_logistico,X_train,y_train)
        return modelo


def modeloXGboost(X_train,y_train):
        modelo_xgboost = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        param_grid_xgboost = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0]
    }
        modelo = modelo_xgboost
        modelo = entrenar_modelo(modelo,param_grid_xgboost,X_train,y_train)
        return modelo

def salvarModelo(modelo,path):
        print(path)
        pickle.dump(modelo, open(path, 'wb'))

if __name__ == '__main__':
        preProcesedPath = sys.argv[1]
        modelPath = sys.argv[2]

        X_train = pd.read_csv(preProcesedPath+"X_train.csv")
        y_train = pd.read_csv(preProcesedPath+"y_train.csv")

        modeloLogRegresion = modeloRlog(X_train,y_train)
        modeloXG = modeloXGboost(X_train,y_train)

        salvarModelo(modeloLogRegresion,modelPath+"modeloRegLog.sav")
        salvarModelo(modeloXG,modelPath+"modeloXGBoost.sav")
        