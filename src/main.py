from typing import List, Dict, cast
import pandas as pd
import random
from base_conocimiento.load_data import cargar_datos_base
from operators.seleccion import seleccion_torneo
from operators.cruza import cruza_poblacion
from operators.mutation import mutar_poblacion
from operators.poda import poda
from utils.evaluar_poblacion import evaluar_poblacion
from utils.fitnes_general import calcular_fitnes_general


#base de conocimiento 
df_jugadores, df_sinergia, reglas_torneo = cargar_datos_base()
df_distribucion_en_modos = cast(Dict[str, Dict[str, int]], reglas_torneo.get("roles_ideales"))
pesos_fitness = cast( Dict[str, float], reglas_torneo.get("pesos_fitness"))
jugador_unico = reglas_torneo.get("jugador_unico", True)


def generar_poblacion() -> List[List[int]]:
    team_size = reglas_torneo.get("tamaño_equipo", 5)
    
    jugadores = df_jugadores["id"].tolist()
    num_equipos = len(jugadores)// team_size
    
    random.shuffle(jugadores)
    poblacion = []

    for i in range(num_equipos):
        equipo = jugadores[i * team_size : (i + 1) * team_size]
        poblacion.append(equipo)

    return poblacion


if __name__ == "__main__":
    
    poblacion_inicial = generar_poblacion()
    resultados_iniciales = evaluar_poblacion(poblacion_inicial, df_jugadores, df_sinergia, df_distribucion_en_modos)

    # Calcular fitness general
    datos_equipos = []
    fitnesses = []
    for i, (rendimiento, sinergia, promedio_roles) in enumerate(resultados_iniciales):
        fitness = calcular_fitnes_general(rendimiento, sinergia, promedio_roles, pesos_fitness)
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
    print("\n📊 Población Inicial:")
    print(df_resultados.to_string(index=False))

    # Selección por torneo
    tamaño_torneo = 10
    num_selecciones = 10
    seleccionados = seleccion_torneo(poblacion_inicial, fitnesses, tamaño_torneo, num_selecciones)

    fitness_seleccionados = []
    for equipo in seleccionados:
        idx = poblacion_inicial.index(equipo)
        fitness_seleccionados.append(fitnesses[idx])

    df_seleccionados = pd.DataFrame({
        "Equipo": [poblacion_inicial.index(eq) + 1 for eq in seleccionados],
        "Jugadores": seleccionados,
        "Fitness General": [round(fit, 3) for fit in fitness_seleccionados]
    })
    print("\n🏆 Equipos Seleccionados (Torneo):")
    print(df_seleccionados.to_string(index=False))

    # 🚼 Cruza
    hijos = cruza_poblacion(seleccionados, jugador_unico)
    resultados_hijos = evaluar_poblacion(hijos, df_jugadores, df_sinergia, df_distribucion_en_modos)
    df_cruza = pd.DataFrame([
        {
            "Hijo": i + 1,
            "Jugadores": hijos[i],
            "Fitness General": round(calcular_fitnes_general(*res, pesos_fitness), 3)
        }
        for i, res in enumerate(resultados_hijos)
    ])
    print("\n🔀 Resultados de la Cruza:")
    print(df_cruza.to_string(index=False))

    # 🧬 Mutación
    jugadores = df_jugadores["id"].tolist()
    mutantes = mutar_poblacion(hijos, jugadores, jugador_unico)
    resultados_mutantes = evaluar_poblacion(mutantes, df_jugadores, df_sinergia, df_distribucion_en_modos)
    df_mutacion = pd.DataFrame([
        {
            "Mutante": i + 1,
            "Jugadores": mutantes[i],
            "Fitness General": round(calcular_fitnes_general(*res, pesos_fitness), 3)
        }
        for i, res in enumerate(resultados_mutantes)
    ])
    print("\n🧬 Resultados de la Mutación:")
    print(df_mutacion.to_string(index=False))

    # 🌿 Poda (nueva población)
    nueva_poblacion = poda(poblacion_inicial, mutantes, df_jugadores, df_sinergia, df_distribucion_en_modos, pesos_fitness)
    resultados_nueva_poblacion = evaluar_poblacion(nueva_poblacion, df_jugadores, df_sinergia, df_distribucion_en_modos)
    df_poda = pd.DataFrame([
        {
            "Nuevo Equipo": i + 1,
            "Jugadores": nueva_poblacion[i],
            "Fitness General": round(calcular_fitnes_general(*res, pesos_fitness), 3)
        }
        for i, res in enumerate(resultados_nueva_poblacion)
    ])
    print("\n🌿 Resultados de la Poda (Nueva Población):")
    print(df_poda.to_string(index=False))
