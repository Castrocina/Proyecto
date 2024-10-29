# Importar librerias
import numpy as np # Libreria para manejar arreglos de datos, las columnas de los data frames
import pandas as pd # Libreria para manejar conjuntos de datos
from sklearn.pipeline import Pipeline # libreria para generar un pipeline de datos
from sklearn.impute import SimpleImputer # libreria para imputar los datos
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer # libreria para preprocesar los datos
from sklearn.compose import ColumnTransformer # libreria para transformar columnas de un data frame
from sklearn.preprocessing import LabelEncoder # libreria para hacer el One Hot encoder
from loadParams import load_params # Libreria Custom para cargar los parametros del archivo params.yaml
import pickle # Libreria para guardar artefactos de python


def crearPipelinePreprocesamientoX():
        """
        Función para crear el pipeline de preprocesamiento de los datos de entrada

        Con las siguientes consideraciones:

        Columnas Númericas con skew, que son las siguientes ("Bilirubin","Cholesterol","Albumin","Copper","Alk_Phos","SGOT","Tryglicerides","Platelets","Prothtombin"):
            1.- Imputar valores con los promedios
            2.- Logaritmo para ajustar skew
            3.- Scaler para scalra y normalizar la distrubyucion

        Columnas Numericas sin skew, que son las siguientes ("N_Days", "Age"):
            1.- Imputar valores con los promedios
            2.- Scaler para scalar y normalizar la distribución

        Columnas no Numericas, que son las siguientes ("Drug", "Ascites","Hepatomegaly", "Spiders", Edema ):
            1.- OneHotEncoder

        Quitaremos las siguientes columnas "ID", "Sex"
        Stage es ordinal, por lo que se dejara como esta

        """
        columnas_numericas_skew = ["Bilirubin", "Cholesterol", "Copper", "Alk_Phos", "SGOT", "Tryglicerides"]
        columnas_numericas_no_skew = ["N_Days", "Age", "Albumin", "Platelets", "Prothrombin"]
        columnas_categoricas = ["Drug", "Sex", "Ascites", "Hepatomegaly", "Spiders", "Edema", "Stage"]
        pipeline_numerico_skew = Pipeline(steps=[
            ('imputador', SimpleImputer(strategy='median')),
            ('log_transform', FunctionTransformer(np.log1p, validate=False)),
            ('escalador', StandardScaler())
        ])
        pipeline_numerico_no_skew = Pipeline(steps=[
            ('imputador', SimpleImputer(strategy='median')),
            ('escalador', StandardScaler())
        ])
        pipeline_categorico = Pipeline(steps=[
            ('imputador', SimpleImputer(strategy='most_frequent')),
            ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore'))
        ])
        transformador_columnas = ColumnTransformer(transformers=[
            ('num_skew', pipeline_numerico_skew, columnas_numericas_skew),
            ('num_no_skew', pipeline_numerico_no_skew, columnas_numericas_no_skew),
            ('cat', pipeline_categorico, columnas_categoricas)
        ], remainder='passthrough')

        return transformador_columnas

def crearPipelinePreprocesamientoy():
    """
        Función para crear el pipeline de preprocesamiento de los datos objetivo, haciendo un Ordinal encoder

    """
    label_encoder = LabelEncoder()
    return label_encoder


if __name__ == '__main__':
    parametros = load_params()
    base_path=parametros["data"]["basePath"]
    preprocesado_path = parametros["data"]["preprocesdePath"]
    path_pipelines = parametros["pipelines"]["path"]


    X_test = pd.read_csv(base_path+"X_test.csv")
    y_test = pd.read_csv(base_path+"y_test.csv").values.ravel()
    X_val = pd.read_csv(base_path+"X_val.csv")
    y_val = pd.read_csv(base_path+"y_val.csv").values.ravel()
    X_train = pd.read_csv(base_path+"X_train.csv")
    y_train = pd.read_csv(base_path+"y_train.csv").values.ravel()

    x_preprocess_pipeline = crearPipelinePreprocesamientoX()
    x_preprocess_pipeline.fit(X_train)
    y_preprocess_pipeline = crearPipelinePreprocesamientoy()
    y_preprocess_pipeline.fit(y_train)
    
    pickle.dump(x_preprocess_pipeline, open(path_pipelines+"preprocesamiento_X.sav", 'wb'))
    pickle.dump(y_preprocess_pipeline, open(path_pipelines+"preprocesamiento_y.sav", 'wb'))

    X_test = x_preprocess_pipeline.transform(X_test)
    y_test = y_preprocess_pipeline.transform(y_test)
    X_val = x_preprocess_pipeline.transform(X_val)
    y_val = y_preprocess_pipeline.transform(y_val)
    X_train = x_preprocess_pipeline.transform(X_train)
    y_train = y_preprocess_pipeline.transform(y_train)

    pd.DataFrame(X_train).to_csv(preprocesado_path+"X_train.csv", index=False)
    pd.DataFrame(y_train).to_csv(preprocesado_path+"y_train.csv", index=False)
    pd.DataFrame(X_val).to_csv(preprocesado_path+"X_val.csv", index=False)
    pd.DataFrame(y_val).to_csv(preprocesado_path+"y_val.csv", index=False)
    pd.DataFrame(X_test).to_csv(preprocesado_path+"X_test.csv", index=False)
    pd.DataFrame(y_test).to_csv(preprocesado_path+"y_test.csv", index=False)


