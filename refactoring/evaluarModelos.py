# Importar librerias
import matplotlib.pyplot as plt # Libreria para 
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
import pickle
import pandas as pd
from loadParams import load_params
import mlflow
import json
import shap

metricasFinales={"entrenamiento":{},"validacion":{},"prueba":{}}

class evaluarModelo():
    """
        Clase para evaluar un modelo

        Atributos:
            modelo:         Modelo a evaluar
            X_train:        DataFrame Conjunto de datos de entrada de entrenamiento
            y_train:        DataFrame Conjunto de datos objetivo de entrenamiento
            X_val:          DataFrame Conjunto de datos de entrada de validación
            y_val:          DataFrame Conjunto de datos objetivo de validación
            X_test:         DataFrame Conjunto de datos de entrada de prueba
            y_test:         DataFrame Conjunto de datos objetivo de prueba
            tipoModelo:     String indicando que tipo de modelo se va a evaluar
            logToMLFlow:    Booleano para indicar si se va a loggear en MLFlow

        Metodos:
            evaluar:                Ejecuta todos los metodos necesarios para evaluar el modelo  
            matriz_de_confusion:    Genera la matriz de confusión de todos los conjuntos de datos
            metricasDeRendimiento:  Genera lasmetricas de rendimiento de todos los conjuntos de datos
            logModeloAMLFlow:       Logea parametros, metricas y modelo a MLFlow
            explicarModelo:         Realiza la gráfica de shap para explicar el modelo

    """
    def __init__(self,modelo,X_train,y_train,X_val,y_val,X_test,y_test,tipoModelo,logToMLFlow):
         self.modelo = modelo
         self.X_train = X_train
         self.y_train=y_train
         self.X_val=X_val
         self.y_val=y_val
         self.X_test=X_test
         self.y_test=y_test
         self.tipoModelo = tipoModelo
         self.logToMLFlow = logToMLFlow
         self.metricas = {"entrenamiento":{},"validacion":{},"prueba":{}}


    def evaluar(self):
        print(f'Evaluado Modelo {self.tipoModelo}')
        y_pred_test = self.modelo.predict(self.X_test)
        y_pred_val = self.modelo.predict(self.X_val)
        y_pred_train = self.modelo.predict(self.X_train)
        self.matriz_de_confuision(self.y_train,y_pred_train,"entrenamiento",self.tipoModelo)
        self.matriz_de_confuision(self.y_val,y_pred_val,"validacion",self.tipoModelo)
        self.matriz_de_confuision(self.y_test,y_pred_test,"prueba",self.tipoModelo)
        self.precision_train,self.recall_train,self.f1_train = self.metricasDeRendimiento(self.y_train,y_pred_train,"entrenamiento")
        self.precision_val,self.recall_val,self.f1_val =self.metricasDeRendimiento(self.y_val,y_pred_val,"validacion")
        self.precision_test,self.recall_test,self.f1_test =self.metricasDeRendimiento(self.y_test,y_pred_test,"prueba")
        metricasFinales["entrenamiento"][f"{self.tipoModelo}_precision_entrenamiento"] = self.precision_train
        metricasFinales["entrenamiento"][f"{self.tipoModelo}_recall_entrenamiento"] = self.recall_train
        metricasFinales["entrenamiento"][f"{self.tipoModelo}_f1_entrenamiento"] = self.f1_train
        metricasFinales["validacion"][f"{self.tipoModelo}_precision_validacion"] = self.precision_val
        metricasFinales["validacion"][f"{self.tipoModelo}_recall_validacion"] = self.recall_val
        metricasFinales["validacion"][f"{self.tipoModelo}_f1_validacion"] = self.f1_val
        metricasFinales["prueba"][f"{self.tipoModelo}_precision_prueba"] = self.precision_test
        metricasFinales["prueba"][f"{self.tipoModelo}_recall_prueba"] = self.recall_test
        metricasFinales["prueba"][f"{self.tipoModelo}_f1_prueba"] = self.f1_test
        if self.logToMLFlow:
            self.logModeloAMLFlow()

    def matriz_de_confuision(self,y,ypred,tipoDeSetDeDatos,tipoModelo):
        # Matriz de confusión
        cm = confusion_matrix(y, ypred)
        figure = plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f"Matriz de Confusión - Conjunto de {tipoDeSetDeDatos} {tipoModelo}")
        plt.xlabel("Predicción")
        plt.ylabel("Real")
        if self.logToMLFlow:
            figure.savefig(f"./docs/confusion_matrixes/{tipoModelo}_{tipoDeSetDeDatos}.png")
            mlflow.log_figure(figure,f"{tipoModelo}_{tipoDeSetDeDatos}.png")
        else:
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

        return precision,recall,f1

    def logModeloAMLFlow(self):
        hyperParametrosDelModelo = self.modelo.get_params()
        for parametro in hyperParametrosDelModelo:
                mlflow.log_param(f"{parametro} {self.tipoModelo}",hyperParametrosDelModelo[parametro])
        mlflow.log_metric(f'precision entrenamiento {self.tipoModelo}',self.precision_train)
        mlflow.log_metric(f'recall entrenamiento {self.tipoModelo}',self.recall_train)
        mlflow.log_metric(f'f1 entrenamiento {self.tipoModelo}',self.f1_train)
        mlflow.log_metric(f'precision validacion {self.tipoModelo}',self.precision_val)
        mlflow.log_metric(f'recall validacion {self.tipoModelo}',self.recall_val)
        mlflow.log_metric(f'f1 validacion {self.tipoModelo}',self.f1_val)
        mlflow.log_metric(f'precision prueba {self.tipoModelo}',self.precision_test)
        mlflow.log_metric(f'recall prueba {self.tipoModelo}',self.recall_test)
        mlflow.log_metric(f'f1 prueba {self.tipoModelo}',self.f1_test)
        mlflow.sklearn.log_model(self.modelo, f"{self.tipoModelo}_model")

    def explicarModelo(self,Xtest,tipoModelo):
        explainer = shap.Explainer(self.model, Xtest)
        shap_values = explainer(Xtest)
        fig = shap.summary_plot(shap_values, X_test, plot_type="bar", show=not self.logToMLFlow)
        plt.title(f"Shap {tipoModelo}")
        if self.logToMLFlow:
            fig.savefig(f"./docs/shap_plot/shap_{tipoModelo}.png")
            mlflow.log_figure(fig,f"shap_{tipoModelo}.png")
        else:
            plt.show()




def logDataInMlflow(dataframe,context,source):
    """
        Función para loggear los set de datos a MLFlow

        parametros:
            dataframe:  El set de datos a guardar en MLFlow
            context:    El contexto del conjunto de datos que se esta enviando, por ejemplo pruebas

    """
    print(source)
    dataset = mlflow.data.from_pandas(dataframe,source=source)

    mlflow.log_input(dataset,context=context)

def cargarModelosyDatos():
    parametros = load_params()
    preprocesado_path = parametros["data"]["preprocesdePath"]
    modelos_path = parametros["modelos"]["path"]
    pipelines_path = parametros["pipelines"]["path"]

    X_train = pd.read_csv(preprocesado_path+"X_train.csv")
    y_train = pd.read_csv(preprocesado_path+"y_train.csv")
    X_val = pd.read_csv(preprocesado_path+"X_val.csv")
    y_val = pd.read_csv(preprocesado_path+"y_val.csv")
    X_test = pd.read_csv(preprocesado_path+"X_test.csv")
    y_test = pd.read_csv(preprocesado_path+"y_test.csv")

    with open(modelos_path+'modeloRegLog.sav', 'rb') as f:
        modeloRLog = pickle.load(f)

    with open(modelos_path+'modeloXGBoost.sav', 'rb') as f:
        modeloXGBoost = pickle.load(f)

    with open(pipelines_path+'preprocesamiento_X.sav', 'rb') as f:
        x_preprocess_pipeline = pickle.load(f)

    with open(pipelines_path+'preprocesamiento_y.sav', 'rb') as f:
        y_preprocess_pipeline = pickle.load(f)

    
    return X_train,y_train,X_val,y_val,X_test,y_test,modeloRLog,modeloXGBoost,x_preprocess_pipeline,y_preprocess_pipeline

        



if __name__ == '__main__':
    parametros = load_params()
    X_train,y_train,X_val,y_val,X_test,y_test,modeloRLog,modeloXGBoost,x_preprocess_pipeline,y_preprocess_pipeline = cargarModelosyDatos()

    mlflow.set_tracking_uri(parametros['mlflow']['tracking_uri'])
    experiment = mlflow.set_experiment(parametros['mlflow']['experiment_name'])
    

    with mlflow.start_run(experiment_id=experiment.experiment_id,run_name=parametros['mlflow']['run_name']):
        logDataInMlflow(X_train,"input train",preprocesado_path+"X_train.csv")
        logDataInMlflow(y_train,"target train",preprocesado_path+"y_train.csv")
        logDataInMlflow(X_val,"input val",preprocesado_path+"X_val.csv")
        logDataInMlflow(y_val,"target val",preprocesado_path+"y_val.csv")
        logDataInMlflow(X_test,"input test",preprocesado_path+"X_test.csv")
        logDataInMlflow(y_test,"target test",preprocesado_path+"y_test.csv")

        mlflow.sklearn.log_model(x_preprocess_pipeline, "X_preprocess_pipeline")
        mlflow.sklearn.log_model(y_preprocess_pipeline, "y_preprocess_pipeline")

        evaluarLogReg = evaluarModelo(modeloRLog,X_train,y_train,X_val,y_val,X_test,y_test,"LogRegresion",True)
        evaluarXGBoost = evaluarModelo(modeloXGBoost,X_train,y_train,X_val,y_val,X_test,y_test,"XGBoost",True)
        evaluarLogReg.evaluar()
        evaluarXGBoost.evaluar()

    mlflow.end_run()

    json_object = json.dumps(metricasFinales, indent=4)
    with open("metricas.json", "w") as outfile:
        outfile.write(json_object)


    
    