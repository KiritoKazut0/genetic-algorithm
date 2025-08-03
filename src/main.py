from typing import List, Dict, cast
import pandas as pd
import random
import matplotlib.pyplot as plt  
from base_conocimiento.load_data import cargar_datos_base
from operators.seleccion import seleccion_torneo
from operators.cruza import cruza_poblacion
from operators.mutation import mutar_poblacion
from operators.poda import poda
from utils.evaluar_poblacion import evaluar_poblacion
from utils.fitnes_general import calcular_fitnes_general

# Cargar datos base (existente)
df_jugadores, df_sinergia, reglas_torneo = cargar_datos_base()
df_distribucion_en_modos = cast(Dict[str, Dict[str, int]], reglas_torneo.get("roles_ideales"))
pesos_fitness = cast(Dict[str, float], reglas_torneo.get("pesos_fitness"))
jugador_unico = reglas_torneo.get("jugador_unico", True)

def generar_poblacion() -> List[List[int]]:
    team_size = reglas_torneo.get("tamaño_equipo", 5)
    jugadores = df_jugadores["id"].tolist()
    num_equipos = len(jugadores) // team_size
    random.shuffle(jugadores)
    return [jugadores[i*team_size:(i+1)*team_size] for i in range(num_equipos)]

if __name__ == "__main__":
    poblacion_actual = generar_poblacion()
    historial_fitness = []

    for generacion in range(1, 80):
        resultados = evaluar_poblacion(poblacion_actual, df_jugadores, df_sinergia, df_distribucion_en_modos)
        fitnesses = [calcular_fitnes_general(rend, sin, rol, pesos_fitness) for rend, sin, rol in resultados]

        # Registro de métricas
        historial_fitness.append({
            "generacion": generacion,
            "mejor": max(fitnesses),
            "peor": min(fitnesses),
            "promedio": sum(fitnesses)/len(fitnesses)
        })

        # Operadores genéticos (existente)
        seleccionados = seleccion_torneo(poblacion_actual, fitnesses, tamaño_torneo=2, num_selecciones=20)
        hijos = cruza_poblacion(seleccionados, jugador_unico)
        mutantes = mutar_poblacion(hijos, df_jugadores["id"].tolist(), jugador_unico)
        poblacion_actual = poda(poblacion_actual, mutantes, df_jugadores, df_sinergia, df_distribucion_en_modos, pesos_fitness)

    # Creación del DataFrame y gráfica
    df_historial = pd.DataFrame(historial_fitness)
    
    # Configuración de la gráfica
    plt.figure(figsize=(12, 6))
    plt.plot(df_historial['generacion'], df_historial['mejor'], 'g-', label='Mejor Fitness', linewidth=2)
    plt.plot(df_historial['generacion'], df_historial['promedio'], 'b-', label='Promedio', linewidth=2)
    plt.plot(df_historial['generacion'], df_historial['peor'], 'r-', label='Peor Fitness', linewidth=2)
    
    plt.title('Evolución del Fitness por Generación', fontsize=14)
    plt.xlabel('Generación', fontsize=12)
    plt.ylabel('Fitness', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.xticks(range(0, 101, 10))
    
    # Mostrar y guardar
    plt.tight_layout()
    plt.savefig('evolucion_fitness.png')
    plt.show()
    
    # Guardar datos
    df_historial.to_csv("historial_fitness.csv", index=False)