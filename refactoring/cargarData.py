# Importar Librerias
from EDA import EDA # Libreria Custom para realizar el EDA de los datos
import pandas as pd # Libreria para manejar archivos de datos y datos
from loadParams import load_params # Libreria custom, para leer los parametros proporcionados en el archivo params.yaml

def cargar_datos(csvpath):
        """Función para cargar los datos a un dataframe de pandas y ejecutar la exploración básica del set de datos.

        Params:
                csvpath:        Path del csv origen de los datos

        Returns:
                datos:          DataFrame de pandas con los datos leidos del csv
        """

        datos = pd.read_csv(csvpath)
        EDA.explorarDataFrame(datos)
        return datos

# Sección de código que se ejecuta al ejecutar este archivo
if __name__ == '__main__':
        parametros = load_params()
        base_path=parametros["data"]["basePath"]
        path_descarga=parametros["data"]["downloadPath"]
        nombre_archivo=parametros["data"]["cirrhosisNombreArchivo"]
        archivo_csv_descargado=path_descarga+nombre_archivo+".csv"
        archivo_csv_base = base_path+nombre_archivo+".csv"

        datos = cargar_datos(archivo_csv_descargado)
        datos.to_csv(archivo_csv_base,index=False)
