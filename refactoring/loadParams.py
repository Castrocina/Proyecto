# Importar librerias
import yaml # Libreria para manejar archivos yaml

def load_params():
    """Función para cargar como un diccionario de python el archivo params.yaml

    Returns:
        cfg:    Diccionario de python que contiene todos los parametros del archivo params.yaml respetando sus herarquias
    """
    with open("params.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg