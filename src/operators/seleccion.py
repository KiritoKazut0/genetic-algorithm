import random
from typing import List

def seleccion_torneo(poblacion, fitnesses, tamaño_torneo, num_selecciones):
    # Ordenar por fitness descendente
    equipos_ordenados = sorted(zip(poblacion, fitnesses), key=lambda x: x[1], reverse=True)
    # Tomar exactamente num_selecciones mejores
    return [equipo for equipo, _ in equipos_ordenados[:num_selecciones]]