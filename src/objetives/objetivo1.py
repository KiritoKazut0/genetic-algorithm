from typing import List
import pandas as pd

def promedio_equipo_por_modo_juego(equipo_formado: List[int], df: pd.DataFrame) -> float:
    modos = [
        "rendimiento_hardpoint",
        "rendimiento_domination",
        "rendimiento_control",
        "rendimiento_search_destroy"
    ]
    
    # Filtra el DataFrame para obtener solo los jugadores cuyo 'id' está en equipo_formado
    df_equipo = df[df["id"].isin(equipo_formado)]
    
    suma = 0
    # Itera sobre cada modo de juego
    for modo in modos:
        # Calcula el promedio del rendimiento del equipo en ese modo
        promedio = df_equipo[modo].mean()
        #  suma total
        suma += promedio
    
    # Divide la suma total entre la cantidad de modos para obtener el fitness final
    fitness_final = suma / len(modos)
    return fitness_final/100
