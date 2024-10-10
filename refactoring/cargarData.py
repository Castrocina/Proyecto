from EDA import EDA
import pandas as pd
import sys

def cargar_datos(csvpath):
        datos = pd.read_csv(csvpath)
        EDA.explorarDataFrame(datos)
        return datos

if __name__ == '__main__':
        datos = cargar_datos(sys.argv[1])
        datos.to_csv(sys.argv[2],index=False)
