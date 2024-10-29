# Importar librerias
import os # Libreria para poder manejar archivos
from urllib.request import urlretrieve # Libreria para descargar información de un URL
from zipfile import ZipFile # Libreria para manejar archivos ZIP
from loadParams import load_params # Libreria custom, para leer los parametros proporcionados en el archivo params.yaml

class descargarDataDeZipACSV:
    """Descargar un archivo ZIP de una URL proporcionada y extraer su contenido a un csv, al instanciar la clase.
        FUnciona solo para archivos ZIP que tienen un solo CSV.

    Attributos:
        url         URL de donde se descargara el archivo ZIP.
        zippath     Path donde se guardara temporalmente el archivo ZIP
        csvpath     Path donde se extraera el archivo csv

    Metodos:
        descargarDeUrl: Descarga el archivo zip del URL proprocionado al instanciar la clase
        extraerDeZip:   Extrae el archivo ZIP descargado al path del csv
        borrarZip:      Borra el ZIP
    """
    def __init__(self,url,zippath,csvpath):
        self.url = url
        self.zippath = zippath
        self.csvpath = csvpath
        self.descargarDeUrl()
        self.extraerDeZip()
        self.borrarZip()

    def descargarDeUrl(self):
        urlretrieve(self.url,self.zippath)

    def extraerDeZip(self):
        with ZipFile(self.zippath) as zObject: 
                zObject.extractall(path=self.csvpath)
    
    def borrarZip(self):
        os.remove(self.zippath)

# Sección de código que se ejecuta al ejecutar este archivo
if __name__ == '__main__':
    parametros = load_params()
    url=parametros["data"]["url"]
    path_descarga=parametros["data"]["downloadPath"]
    nombre_archivo=parametros["data"]["cirrhosisNombreArchivo"]
    zippath=path_descarga+nombre_archivo+".zip"

    descargarDataDeZipACSV(url,zippath,path_descarga)