import random
from typing import List

def mutacion_multiple(
    individuo: List[int],
    jugadores_totales: List[int],
    tasa_mutacion: float = 0.1
    
    ) -> List[int]:
    
    jugadores_disponibles = list(set(jugadores_totales) - set(individuo))
    
    for i in range(len(individuo)):
        if random.random() < tasa_mutacion:
            if jugadores_disponibles:
                nuevo_jugador = random.choice(jugadores_disponibles)
                jugadores_disponibles.append(individuo[i])
                jugadores_disponibles.remove(nuevo_jugador)
                individuo[i] = nuevo_jugador
                
    return individuo


def mutar_poblacion(
    poblacion: List[List[int]],
    jugadores_totales: List[int],
    tasa_mutacion : float =0.1
    
    ) -> List[List[int]]:
    
    nueva_poblacion = []
    for individuo in poblacion:
        individuo_mutado = mutacion_multiple(individuo.copy(), jugadores_totales, tasa_mutacion)
        nueva_poblacion.append(individuo_mutado)
    return nueva_poblacion
