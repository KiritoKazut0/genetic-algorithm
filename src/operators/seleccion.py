import random
from typing import List

def seleccion_torneo(
    poblacion: List[List[int]], 
    fitnesses: List[float], 
    tamaño_torneo: int, 
    num_selecciones: int
) -> List[List[int]]:
    
    seleccionados = []
    participantes_disponibles = list(zip(poblacion, fitnesses))  # Lista de (equipo, fitness)

    while len(seleccionados) < num_selecciones and len(participantes_disponibles) >= tamaño_torneo:
        # Seleccionar aleatoriamente sin reemplazo para torneo solo de equipos disponibles
        participantes = random.sample(participantes_disponibles, tamaño_torneo)
        
        # Elegir al ganador del torneo (mayor fitness)
        ganador = max(participantes, key=lambda x: x[1])
        
        # Añadir equipo ganador a seleccionados
        seleccionados.append(ganador[0])
        
        # Eliminar al ganador de la lista de participantes disponibles para que no vuelva a competir
        participantes_disponibles = [p for p in participantes_disponibles if p[0] != ganador[0]]

    return seleccionados
