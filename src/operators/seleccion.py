import random
import pandas as  pd 
from typing import List

def seleccion_torneo(
    poblacion: List[List[int]],
    fitnesses: list[float],
    tamaño_torneo: int,
    num_selecciones: int) -> list[List[int]]:
    # Ordenar por fitness descendente
    equipos_ordenados = sorted(zip(poblacion, fitnesses), key=lambda x: x[1], reverse=True)
    # Tomar exactamente num_selecciones mejores
    return [equipo for equipo, _ in equipos_ordenados[:num_selecciones]]