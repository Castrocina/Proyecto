from pydantic import BaseModel
from typing import List



class CirrhosisData(BaseModel):
    N_Days: float
    Drug: str
    Age: float
    Sex: str
    Ascites: str
    Hepatomegaly:str
    Spiders: str
    Edema:str
    Bilirubin: float
    Cholesterol: float
    Albumin: float
    Copper:float
    Alk_Phos:float
    SGOT:float
    Tryglicerides: float
    Platelets: float
    Prothrombin:float
    Stage:float

class PredictionRequest(BaseModel):
    data: CirrhosisData