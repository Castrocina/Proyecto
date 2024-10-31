import pytest
from cargarData import cargarData
from cirrhosis_schema import cirrhosis_schema
import numpy as np


datos = cargarData()
datos = datos.drop(['ID'],axis=1)
schema = cirrhosis_schema()

def test_inputData_min_max():
    maxValues = datos.max(axis=0,skipna=True, numeric_only=True)
    minValues = datos.min(axis=0,skipna=True, numeric_only=True)

    for feature in datos.select_dtypes(include=np.number).columns:
        assert maxValues[feature] <= schema[feature]['range']['max']
        assert minValues[feature] >= schema[feature]['range']['min']

def test_input_Data_types():
    tipos = datos.dtypes
    for feature in datos.columns:
        assert tipos[feature]==schema[feature]["dtype"]






