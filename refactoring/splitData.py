# Importar librerias
from EDA import EDA # Libreria Custom para realizar EDA
from sklearn.model_selection import train_test_split # Libreria para separar set de datos
from sklearn.preprocessing import LabelEncoder # libreria para realizar el OneHot encoder
import pandas as pd # Libreria para manejar archivos de datos
from loadParams import load_params # Libreria Custom para cargar los parametros del archivo params.yaml

def dividir_datos(datos, test_size=0.3, validation_size=0.5):
        """
        Función para separar los datos en entrenamiento, validación y prueba y ejecutar el EDA con los datos de entrenamiento

        Parametros:
                datos:          Dataframe con los datos a separar
                test_size:      Porcentaje de los datos que se utilizaran para crear sets de validación y prueba, por default 30%
                validation_size Porcentaje de datos para validación del porcentaje de datos para utilizar del se de validación y prueba, por default 50% 
        
        Returns:
                X_test:         Data Frame con los datos de entrada de prueba
                y_test:         Data frame con los datos objetivo de prueba
                X_val:          Data frame con los datos de entrada de validación
                y_val:          Data frame con los datos objetivo de validación
                X_train:        Data frame con los datos de entrada de entrenamiento
                y_trai:         Data frame con los datos objetivo de validación
        """

        X = datos.drop(columns=["Status", 'ID'])
        y = datos["Status"]

        # División en entrenamiento (70%), validación (15%) y prueba (15%)
        X_train, X_test1, y_train, y_test1 = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
        X_val, X_test, y_val, y_test = train_test_split(X_test1, y_test1, test_size=validation_size, random_state=42, stratify=y_test1)

        #Explorar los datos de entrenamiento
        EDA().boxPlotNumericas(X_train)
        EDA().histogramasNumericas(X_train)
        EDA().countPlotCategoricas(X_train)

        labelEncoder = LabelEncoder()

        y_preprocesado_df = pd.DataFrame(
            labelEncoder.fit_transform(y_train), 
            columns=["Status"],
            index=y_train.index
        )

        EDA().mapaDeCorrelacion(X_train,y_preprocesado_df,"Status")
        EDA().boxPlotVSTarget(X_train,y_train,"Status")

        return X_test,y_test,X_val,y_val,X_train,y_train

if __name__ == '__main__':
        parametros = load_params()
        base_path=parametros["data"]["basePath"]
        nombre_archivo=parametros["data"]["cirrhosisNombreArchivo"]
        csv_path=base_path+nombre_archivo+'.csv'
        datos=pd.read_csv(csv_path)
        X_test, y_test, X_val, y_val, X_train, y_train = dividir_datos(datos)
        X_test.to_csv(base_path+"X_test.csv",index=False)
        y_test.to_csv(base_path+"y_test.csv",index=False)
        X_val.to_csv(base_path+"X_val.csv",index=False)
        y_val.to_csv(base_path+"y_val.csv",index=False)
        X_train.to_csv(base_path+"X_train.csv",index=False)
        y_train.to_csv(base_path+"y_train.csv",index=False)

