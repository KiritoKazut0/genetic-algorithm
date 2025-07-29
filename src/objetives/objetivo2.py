import pandas as pd
from typing import List

def sinergia_equipo(equipo_formado: List[int], df_sinergia: pd.DataFrame) -> float:
    suma = 0
    pares_totales = 0

    for i in range(len(equipo_formado)):
        for j in range(i + 1, len(equipo_formado)):
            a = equipo_formado[i]
            b = equipo_formado[j]

            fila = df_sinergia[
                ((df_sinergia["jugador_A"] == a) & (df_sinergia["jugador_B"] == b)) |
                ((df_sinergia["jugador_A"] == b) & (df_sinergia["jugador_B"] == a))
            ]
            
            if not fila.empty:
                suma += fila["sinergia"].values[0]
            pares_totales += 1

    promedio = suma / pares_totales if pares_totales > 0 else 0
    return promedio / 100  # Normalizamos a rango 0 - 1
