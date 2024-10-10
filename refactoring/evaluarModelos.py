import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
import pickle
import sys
import pandas as pd

class evaluarModelo():

    @staticmethod
    def matriz_de_confuision(y,ypred,tipoDeSetDeDatos):
        # Matriz de confusión
        cm = confusion_matrix(y, ypred)
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f"Matriz de Confusión - Conjunto de {tipoDeSetDeDatos}")
        plt.xlabel("Predicción")
        plt.ylabel("Real")
        plt.show()

    @staticmethod
    def metricasDeRendimiento(y,ypred,tipoDeSetDeDatos):
        # Cálculo de métricas con zero_division
        precision = precision_score(y, ypred, average='weighted', zero_division=0)
        recall = recall_score(y, ypred, average='weighted', zero_division=0)
        f1 = f1_score(y, ypred, average='weighted', zero_division=0)

        # Mostrar resultados
        print(f"Precisión de conjunto de {tipoDeSetDeDatos}: {precision:.2f}")
        print(f"Recall de conjunto de {tipoDeSetDeDatos}: {recall:.2f}")
        print(f"Puntuación de conjunto de {tipoDeSetDeDatos}: {f1:.2f}")

if __name__ == '__main__':
    preProcesedPath = sys.argv[1]
    pathModelos = sys.argv[2]

    X_train = pd.read_csv(preProcesedPath+"X_train.csv")
    y_train = pd.read_csv(preProcesedPath+"y_train.csv")
    X_val = pd.read_csv(preProcesedPath+"X_val.csv")
    y_val = pd.read_csv(preProcesedPath+"y_val.csv")
    X_test = pd.read_csv(preProcesedPath+"X_test.csv")
    y_test = pd.read_csv(preProcesedPath+"y_test.csv")

    with open(pathModelos+'modeloRegLog.sav', 'rb') as f:
        modeloRLog = pickle.load(f)

    with open(pathModelos+'modeloXGBoost.sav', 'rb') as f:
        modeloXGBoost = pickle.load(f)

    y_pred_rlog_test = modeloRLog.predict(X_test)
    y_pred_rlog_val = modeloRLog.predict(X_val)
    y_pred_rlog_train = modeloRLog.predict(X_train)
    print("evaluacion modelo regresion logistica")
    evaluarModelo().matriz_de_confuision(y_train,y_pred_rlog_train,"entrenamiento")
    evaluarModelo().matriz_de_confuision(y_val,y_pred_rlog_val,"validacion")
    evaluarModelo().matriz_de_confuision(y_test,y_pred_rlog_test,"prueba")
    evaluarModelo().metricasDeRendimiento(y_train,y_pred_rlog_train,"entrenamiento")
    evaluarModelo().metricasDeRendimiento(y_val,y_pred_rlog_val,"validacion")
    evaluarModelo().metricasDeRendimiento(y_test,y_pred_rlog_test,"prueba")

    y_pred_xg_test = modeloXGBoost.predict(X_test)
    y_pred_xg_val = modeloXGBoost.predict(X_val)
    y_pred_xg_train = modeloXGBoost.predict(X_train)
    print("evaluacion modelo XGBoost")
    evaluarModelo().matriz_de_confuision(y_train,y_pred_xg_test,"entrenamiento")
    evaluarModelo().matriz_de_confuision(y_val,y_pred_xg_val,"validacion")
    evaluarModelo().matriz_de_confuision(y_test,y_pred_xg_test,"prueba")
    evaluarModelo().metricasDeRendimiento(y_train,y_pred_xg_test,"entrenamiento")
    evaluarModelo().metricasDeRendimiento(y_val,y_pred_xg_val,"validacion")
    evaluarModelo().metricasDeRendimiento(y_test,y_pred_xg_test,"prueba")


    
    