from typing import List, Dict
import pandas as pd
import random
from base_conocimiento.load_data import cargar_datos_base
from operators.seleccion import seleccion_torneo
from operators.cruza import cruza_poblacion
from operators.mutation import mutar_poblacion
from operators.poda import poda
from utils.evaluar_poblacion import evaluar_poblacion
from utils.fitnes_general import calcular_fitnes_general
from ui.graficas import mostrar_evolucion_tiempo_real

def generar_poblacion(jugadores: List[int], team_size: int) -> List[List[int]]:
    num_equipos = len(jugadores) // team_size
    random.shuffle(jugadores)
    return [jugadores[i*team_size:(i+1)*team_size] for i in range(num_equipos)]

def ejecutar_algoritmo_genetico():
    # Cargar datos
    df_jugadores, df_sinergia, reglas_torneo = cargar_datos_base()
    df_distribucion = reglas_torneo["roles_ideales"]
    pesos_fitness = reglas_torneo["pesos_fitness"]
    jugador_unico = reglas_torneo.get("jugador_unico", True)
    team_size = reglas_torneo.get("tamaño_equipo", 5)
    
    # Configuración inicial
    poblacion = generar_poblacion(df_jugadores["id"].tolist(), team_size)
    historial = []
    mejores_equipos = []

    # Configurar gráfica en tiempo real
    grafica = mostrar_evolucion_tiempo_real()
    
    for generacion in range(1, 80):
        # Evaluación
        resultados = evaluar_poblacion(poblacion, df_jugadores, df_sinergia, df_distribucion)
        fitnesses = [calcular_fitnes_general(*res, pesos_fitness) for res in resultados]
        
        # Registrar métricas
        historial.append({
            "generacion": generacion,
            "mejor": max(fitnesses),
            "peor": min(fitnesses),
            "promedio": sum(fitnesses)/len(fitnesses),
            "mejor_equipo": poblacion[fitnesses.index(max(fitnesses))]
        })
        
        # Actualizar gráfica
        grafica.actualizar(
            generacion,
            max(fitnesses),
            sum(fitnesses)/len(fitnesses),
            min(fitnesses)
        )
        
        # Operadores genéticos
        seleccionados = seleccion_torneo(poblacion, fitnesses, tamaño_torneo=2, num_selecciones=20)
        hijos = cruza_poblacion(seleccionados, jugador_unico)
        mutantes = mutar_poblacion(hijos, df_jugadores["id"].tolist(), jugador_unico)
        poblacion = poda(poblacion, mutantes, df_jugadores, df_sinergia, df_distribucion, pesos_fitness)
    

if __name__ == "__main__":
    ejecutar_algoritmo_genetico()