# Importar Librerias
import seaborn as sns # Libreria para generar gráficas mpás avanzadas
import matplotlib.pyplot as plt # Libreria para generar gráficas
import pandas as pd # Libreria para manejar archivos de datos

class EDA():
    """Clase que contiene los metodos necesarios para realizar un EDA completo
    """

    @staticmethod
    def explorarDataFrame(df):
        """
            Metodo para explorar los tipos de datos y la información general de un data frame proporcionado

            parametros:
                df:     Data Frame que contiene los datos
        """
        print(f"Tamaño del dataset: {df.shape}")
        print("Tipos de datos por columna:")
        print(df.dtypes)

        print("Primeras filas:")
        print(df.head())

        print("Porcentaje de valores nulos por columna:")
        valores_nulos_porcentajes = df.isna().mean() * 100
        print(valores_nulos_porcentajes[valores_nulos_porcentajes > 0])

    @staticmethod
    def histogramasNumericas(df):
        """
            Metodo para generar histogramas de todas las columnas de datos númericas del dataframe proporcionado

            parametros:
                df:     Data Frame que contiene los datos
        """
        cat_con = df.select_dtypes(include="number").columns.tolist()[1:]
        fig, axes = plt.subplots(4, 3, figsize=(50, 40))
        axes = axes.ravel()
        for col, ax in zip(df[cat_con], axes):
            sns.histplot(x=df[col], ax=ax, bins=30)
            ax.set(title=f'{col}', xlabel=None)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def boxPlotNumericas(df):
        """
            Metodo para generar boxplots de todas las columnas de datos númericas del dataframe proporcionado

            parametros:
                df:     Data Frame que contiene los datos
        """
        cat_con = df.select_dtypes(include="number").columns.tolist()[1:]
        fig, axes = plt.subplots(4, 3, figsize=(50, 40))
        axes = axes.ravel()
        for col, ax in zip(df[cat_con], axes):
            sns.boxplot(x=df[col], ax=ax)
            ax.set(title=f'{col}', xlabel=None)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def countPlotCategoricas(df):
        """
            Metodo para generar countplots de todas las columnas de datos categoricos (No numericos) del dataframe proporcionado

            parametros:
                df:     Data Frame que contiene los datos
        """
        cat_con = df.select_dtypes(include="object").columns.tolist()[1:]
        fig, axes = plt.subplots(3, 3, figsize=(50, 40))
        axes = axes.ravel()
        for col, ax in zip(df[cat_con], axes):
            sns.countplot(x=df[col], ax=ax)
            ax.set(title=f'{col}', xlabel=None)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def mapaDeCorrelacion(df,targetdf,target_col):
        """
            Metodo para generar el mapa de correlación de pearson

            parametros:
                df:         Data Frame que contiene los datos de entrada
                target:     Data Frame que contiene los datos objetivo
                target_col: String con el nombre de la columna de los datos objetivo 
        """
        df = pd.concat([df,targetdf],axis=1)
        numeric_df = df.select_dtypes(include=['number'])
        if target_col in df.columns:
            numeric_df[target_col] = df[target_col]
        corr = numeric_df.corr()
        plt.figure(figsize=(15, 10))
        sns.heatmap(corr, annot=True, cmap="BuGn", fmt='.2f')
        plt.title('Mapa de Calor de Correlación')
        plt.show()

    @staticmethod
    def boxPlotVSTarget(df,targetdf,target_col):
        """
            Metodo para generar boxplot de la variable objetivo contra las variables categoricas de entrada
            parametros:
                df:         Data Frame que contiene los datos de entrada
                target:     Data Frame que contiene los datos objetivo
                target_col: String con el nombre de la columna de los datos objetivo 
        """
        df = pd.concat([df,targetdf],axis=1)
        cat_con = df.select_dtypes(include="number").columns.tolist()
        fig, axes = plt.subplots(2, 3, figsize=(50, 40))
        axes = axes.ravel()
        for col, ax in zip(cat_con, axes):
            sns.boxplot(data=df, x=col, y=target_col, ax=ax)
            ax.set(title=f'{col} vs {target_col}', xlabel=None)
        plt.tight_layout()
        plt.show()