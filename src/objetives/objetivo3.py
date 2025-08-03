import pandas as pd
from typing import Dict, List

def equilibrio_roles_por_modo(
       equipo_formado: List[int],
        df_jugadores: pd.DataFrame,
        roles_ideales: Dict[str, Dict[str, int]]
) -> Dict[str, float]:
    
    equipo = df_jugadores[df_jugadores['id'].isin(equipo_formado)]
    resultados = {}

    for modo, ideales in roles_ideales.items():
                
        reales = {rol: 0.0 for rol in ideales}

        for _, jugador in equipo.iterrows():
            primario = jugador['rol_primario']
            secundario = jugador['rol_secundario']
            if primario in reales:
                reales[primario] += 1.0
            if secundario in reales:
                reales[secundario] += 0.5

        diferencia = 0
        for rol in ideales:
            diferencia += abs(reales[rol] - ideales[rol])

        total_ideal = sum(ideales.values())
        fitness = max(0, 1 - (diferencia / total_ideal))

        resultados[modo] = round(fitness, 3)

    return resultados
