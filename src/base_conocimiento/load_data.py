from typing import Tuple
import pandas as pd
import json


def cargar_datos_base() -> Tuple [pd.DataFrame, pd.DataFrame, dict] :
    
    df_jugadores = pd.read_csv("../src/base_conocimiento/jugadores.csv")
    df_sinergias = pd.read_csv("../src/base_conocimiento/sinergia_jugadores.csv")

    with open("../src/base_conocimiento/reglas_torneo.json", "r") as file:
        reglas_torneo = json.load(file)

    return df_jugadores, df_sinergias, reglas_torneo
