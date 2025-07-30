import random
from typing import List, Tuple
from utils.crossover_utils import reparar_con_diferencia


def cruza(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")

    longitud = len(padre1)
    punto1 = random.randint(0, longitud - 2)
    punto2 = random.randint(punto1 + 1, longitud - 1)

    hijo1 = padre1[:punto1] + padre2[punto1:punto2+1] + padre1[punto2+1:]
    hijo2 = padre2[:punto1] + padre1[punto1:punto2+1] + padre2[punto2+1:]

    hijo1 = reparar_con_diferencia(hijo1, padre1)
    hijo2 = reparar_con_diferencia(hijo2, padre2)

    return hijo1, hijo2


def cruza_poblacion(equipos: List[List[int]]) -> List[List[int]]: 
    nueva_generacion = []
    
    if len(equipos) % 2 != 0:
        raise ValueError("La cantidad de equipos debe ser par para cruzarlos en pares.")
    
    for i in range(0, len(equipos), 2):
        padre1 = equipos[i]
        padre2 = equipos[i + 1]
        
        hijo1, hijo2 = cruza(padre1, padre2)
        nueva_generacion.append(hijo1)
        nueva_generacion.append(hijo2)
    
    return nueva_generacion


# def cruza_un_punto(equipo1, equipo2):
#     if len(equipo1) != len(equipo2):
#         raise ValueError("Los equipos deben tener la misma longitud para la cruza.")
    
#     punto_cruza = random.randint(1, len(equipo1) - 1) 
#     hijo1 = equipo1[:punto_cruza] + equipo2[punto_cruza:]
#     hijo2 = equipo2[:punto_cruza] + equipo1[punto_cruza:]
    
#     return hijo1, hijo2
