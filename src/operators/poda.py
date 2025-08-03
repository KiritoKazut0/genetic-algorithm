import pandas as pd
from typing import Dict, List
from utils.evaluar_poblacion import evaluar_poblacion
from utils.fitnes_general import calcular_fitnes_general
import random


def poda(
    poblacion_inicial: List[List[int]],
    poblacion_mutada: List[List[int]],
    df_jugadores: pd.DataFrame,
    df_sinergias: pd.DataFrame,
    distribucion_ideal: Dict[str, Dict[str, int]],
    peso_fitnes: Dict[str, float],
    usar_elitismo: bool = True,
    porcentaje_elitismo: float = 0.15,
    porcentaje_aleatorio: float = 0.1
) -> List[List[int]]:
    
    # Evaluación
    evaluacion_inicial = evaluar_poblacion(poblacion_inicial, df_jugadores, df_sinergias, distribucion_ideal)
    evaluacion_mutada = evaluar_poblacion(poblacion_mutada, df_jugadores, df_sinergias, distribucion_ideal)

    # Cálculo de fitness
    fitness_inicial = [(eq, calcular_fitnes_general(f1,f2,f3, peso_fitnes)) 
                      for eq, (f1,f2,f3) in zip(poblacion_inicial, evaluacion_inicial)]
    fitness_mutada = [(eq, calcular_fitnes_general(f1,f2,f3, peso_fitnes)) 
                     for eq, (f1,f2,f3) in zip(poblacion_mutada, evaluacion_mutada)]

    # Combinar y ordenar
    poblacion_total = fitness_inicial + fitness_mutada
    poblacion_ordenada = sorted(poblacion_total, key=lambda x: x[1], reverse=True)

    # Asegurar tamaño par
    n_total = len(poblacion_inicial)
    if n_total % 2 != 0:
        n_total -= 1  # Ajustar a número par

    # Nueva lógica de selección (asegurando paridad)
    n_elite = max(2, int(porcentaje_elitismo * n_total))  # Mínimo 2 elites
    n_elite = n_elite if n_elite % 2 == 0 else n_elite - 1  # Asegurar par
    
    n_aleatorio = max(2, int(porcentaje_aleatorio * n_total))  # Mínimo 2 aleatorios
    n_aleatorio = n_aleatorio if n_aleatorio % 2 == 0 else n_aleatorio - 1
    
    elite = [eq for eq, _ in poblacion_ordenada[:n_elite]]
    
    # Selección aleatoria controlada
    restante_ordenado = [eq for eq, _ in poblacion_ordenada[n_elite:]]
    aleatorios = random.sample(restante_ordenado, min(n_aleatorio, len(restante_ordenado)))
    
    # Completar con mejores del resto (asegurando paridad)
    disponibles = n_total - n_elite - n_aleatorio
    disponibles = disponibles if disponibles % 2 == 0 else disponibles - 1
    no_seleccionados = [eq for eq in restante_ordenado if eq not in aleatorios]
    mejores_resto = no_seleccionados[:disponibles]
    
    poblacion_final = elite + aleatorios + mejores_resto
    
    # Garantizar tamaño correcto (por si acaso)
    return poblacion_final[:n_total] if len(poblacion_final) % 2 == 0 else poblacion_final[:-1]