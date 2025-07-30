from typing import List, Dict, Tuple
import pandas as pd
import json
import random
from objetives import objetivo1, objetivo2, objetivo3
from operators.seleccion import seleccion_torneo
from operators.cruza import cruza_poblacion
from operators.mutation import mutar_poblacion
# from operators.poda import 
from utils.fitnes_general import calcular_fitnes_general



df_jugadores = pd.read_csv("../src/base_conocimiento/jugadores.csv")
df_sinergias = pd.read_csv("../src/base_conocimiento/sinergia_jugadores.csv")

with open("../src/base_conocimiento/distribucion_ideal.json", "r") as file:
    df_distribucion_en_modos = json.load(file)


def generar_poblacion() -> List[List[int]]:
    team_size = 5
    num_equipos = 20

    # Obtener lista de jugadores (IDs)
    jugadores = df_jugadores["id"].tolist()

    # Barajar la lista para mezclar jugadores
    random.shuffle(jugadores)

    poblacion = []

    # Tomar bloques de 5 jugadores para formar cada equipo
    for i in range(num_equipos):
        equipo = jugadores[i * team_size : (i + 1) * team_size]
        poblacion.append(equipo)

    return poblacion

def evaluar_poblacion(
    poblacion: list[list[int]],
    df_jugadores: pd.DataFrame,
    df_sinergias: pd.DataFrame,
    distribucion_ideal: Dict[str, Dict[str, Dict[str, int]]],
):
    resultados = []

    for equipo in poblacion:
        f1 = objetivo1.promedio_equipo_por_modo_juego(equipo, df_jugadores)
        f2 = objetivo2.sinergia_equipo(equipo, df_sinergias)
        f3_dict= objetivo3.equilibrio_roles_por_modo(
            equipo, df_jugadores, distribucion_ideal
        )
        # print(resultados.append((f1,f2,f3_dict)))
        f3 = sum(f3_dict.values()) / len(f3_dict) if f3_dict else 0.0
        resultados.append((f1, f2, f3))

    return resultados


if __name__ == "__main__":
    poblacion_inicial = generar_poblacion()
    resultados_iniciales = evaluar_poblacion(poblacion_inicial, df_jugadores, df_sinergias, df_distribucion_en_modos)

    # Calcular fitness general para cada equipo
    datos_equipos = []
    fitnesses = []
    for i, (rendimiento, sinergia, promedio_roles) in enumerate(resultados_iniciales):
        fitness = calcular_fitnes_general(rendimiento, sinergia, promedio_roles)
        fitnesses.append(fitness)

        datos_equipos.append({
            "Equipo": i + 1,
            "Jugadores": poblacion_inicial[i],
            "Rendimiento": round(rendimiento, 3),
            "Sinergia": round(sinergia, 3),
            "Roles": round(promedio_roles, 3),
            "Fitness General": round(fitness, 3)
        })

    df_resultados = pd.DataFrame(datos_equipos)

    # Mostrar tabla de población inicial (solo IDs de jugadores)
    print("\nPoblación Inicial (Equipos y Jugadores):")
    print(df_resultados[["Equipo", "Jugadores"]].to_string(index=False))

    # Mostrar tabla de evaluación (fitness y objetivos)
    print("\nEvaluación de la Población Inicial:")
    print(df_resultados[["Equipo", "Rendimiento", "Sinergia", "Roles", "Fitness General"]].to_string(index=False))

    # Parámetros para selección por torneo
    tamaño_torneo = 10
    num_selecciones = 10  # Ejemplo: seleccionar 5 equipos

    # Selección usando la función en operators.seleccion (asegúrate que esté importada correctamente)
    seleccionados = seleccion_torneo(poblacion_inicial, fitnesses, tamaño_torneo, num_selecciones)

    # Obtener fitness de los seleccionados para mostrar
    fitness_seleccionados = []
    for equipo in seleccionados:
        idx = poblacion_inicial.index(equipo)
        fitness_seleccionados.append(fitnesses[idx])

    # Crear DataFrame para mostrar seleccionados
    df_seleccionados = pd.DataFrame({
        "Equipo": [poblacion_inicial.index(eq) + 1 for eq in seleccionados],
        "Jugadores": seleccionados,
        "Fitness General": [round(fit,3) for fit in fitness_seleccionados]
    })

    print("\nEquipos seleccionados en torneo:")
    print(df_seleccionados.to_string(index=False))
    
    
    #seccion para ver como se representa la cruza con los demas equipos
    
    df_cruza = cruza_poblacion(seleccionados)
    print("RESULTADOS DE LA CRUZA")
    print(df_cruza)
    
    jugadores = df_jugadores["id"].tolist()
    
    df_mutacion = mutar_poblacion(df_cruza, jugadores )
    print("RESULTADOS DE LA MUTACION")
    print(df_mutacion)