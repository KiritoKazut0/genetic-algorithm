import pandas as pd
from typing import Dict, List
from utils.evaluar_poblacion import evaluar_poblacion
from utils.fitnes_general import calcular_fitnes_general


def poda(
    poblacion_inicial: List[List[int]],
    poblacion_mutada: List[List[int]],
    df_jugadores: pd.DataFrame,
    df_sinergias: pd.DataFrame,
    distribucion_ideal:Dict[str, Dict[str, int]],
    peso_fitnes : Dict[str, float],
    usar_elitismo: bool = True,
    porcentaje_elitismo: float = 0.1,
    
) -> List[List[int]]:
    

    evaluacion_inicial = evaluar_poblacion(poblacion_inicial, df_jugadores, df_sinergias, distribucion_ideal)
    evaluacion_mutada = evaluar_poblacion(poblacion_mutada, df_jugadores, df_sinergias, distribucion_ideal)

    fitness_inicial = [
        (equipo, calcular_fitnes_general(f1, f2, f3, peso_fitnes))
        for equipo, (f1, f2, f3) in zip(poblacion_inicial, evaluacion_inicial)
    ]
    fitness_mutada = [
        (equipo, calcular_fitnes_general(f1, f2, f3, peso_fitnes))
        for equipo, (f1, f2, f3) in zip(poblacion_mutada, evaluacion_mutada)
    ]

    poblacion_total = fitness_inicial + fitness_mutada

    poblacion_ordenada = sorted(poblacion_total, key=lambda x: x[1], reverse=True)

    nueva_poblacion = []

    if usar_elitismo:
        n_elite = int(porcentaje_elitismo * len(poblacion_inicial))
        elite = poblacion_ordenada[:n_elite]
        restante = poblacion_ordenada[n_elite:]
        nueva_poblacion = elite + restante[:len(poblacion_inicial) - n_elite]
    else:
        nueva_poblacion = poblacion_ordenada[:len(poblacion_inicial)]

    return [equipo for equipo, _ in nueva_poblacion]
    
    