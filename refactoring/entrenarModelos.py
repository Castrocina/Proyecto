# Importar Librerias
from sklearn.model_selection import GridSearchCV # libreria para hacer un GridSearch de los hyperparametros del modelo
from sklearn.linear_model import LogisticRegression # libreria para hacer regresion logistica
from xgboost import XGBClassifier # Libreria para utilizar el modelo XGBClasifier
import pickle # libreria para exportar archivos de python
import pandas as pd # Libreria para manejar set de datos
from loadParams import load_params # Libreria custom para importar los parametros del archivo params.yaml

def entrenar_modelo(model,param_grid,X_train,y_train):
        """
        Función para entrenar un modelo proporcionado utilizando Gridsearch con la lista de parametros a evaluar proporcionada y los datos de entrenamiento proporcionados

        Parametros:
                model:          Modelo a entrenar
                param_grid:     Diccionario con los parametros a utilizar en el grid search
                X_train:        Datos de entrada de entrenamiento
                y_train:        Datos objetivo de entrenamiento
        
        Returns:
                grid_search.best_estimator_:         Diccionario con los valores de los hyperparametros del mejor modelo
        """

        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train.ravel())

        return grid_search.best_estimator_

def modeloRlog(X_train,y_train,param_grid_logistico):
        """
        Función para entrenar un modelo deregresion logistica con los datos de entrenamiento proporcionados y los parametros a utilizar en el grid search

        Parametros:
                X_train:                Datos de entrada de entrenamiento
                y_train:                Datos objetivo de entrenamiento
                param_grid_logistico:   Diccionario con los parametros a utilizar en el grid search
        
        Returns:
                modelo: El modelo entrenado de regresion lineal
        """
        
        modelo_logistico = LogisticRegression(max_iter=5000)
        
        modelo = modelo_logistico
        modelo = entrenar_modelo(modelo,param_grid_logistico,X_train,y_train)
        return modelo


def modeloXGboost(X_train,y_train,param_grid_xgboost):
        """
        Función para entrenar un modelo XGBoost con los datos de entrenamiento proporcionados y los parametros a utilizar en el grid search

        Parametros:
                X_train:                Datos de entrada de entrenamiento
                y_train:                Datos objetivo de entrenamiento
                param_grid_xgboost:   Diccionario con los parametros a utilizar en el grid search
        
        Returns:
                modelo: El modelo entrenado de XGBoost
        """

        modelo_xgboost = XGBClassifier(use_label_encoder=True, eval_metric='logloss')
        modelo = modelo_xgboost
        modelo = entrenar_modelo(modelo,param_grid_xgboost,X_train,y_train)
        return modelo

def salvarModelo(modelo,path):
        """
        Función para guardar un modelo proporcionado

        Parametros:
                modelo: Modelo a guardar
                path:   Path donde se guardara el modelo
        """
        pickle.dump(modelo, open(path, 'wb'))

if __name__ == '__main__':
        parametros = load_params()
        preprocesado_path = parametros["data"]["preprocesdePath"]
        modelos_path = parametros["modelos"]["path"]
        param_grid_xgboost = parametros["modelos"]["grid_xgboost"]
        param_grid_logistico = parametros["modelos"]["grid_logistico"]

        X_train = pd.read_csv(preprocesado_path+"X_train.csv")
        y_train = pd.read_csv(preprocesado_path+"y_train.csv").values.ravel()

        modeloLogRegresion = modeloRlog(X_train,y_train,param_grid_logistico)
        modeloXG = modeloXGboost(X_train,y_train,param_grid_xgboost)

        salvarModelo(modeloLogRegresion,modelos_path+"modeloRegLog.sav")
        salvarModelo(modeloXG,modelos_path+"modeloXGBoost.sav")
        
        
