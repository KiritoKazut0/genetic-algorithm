from typing import List, Dict, Tuple
import pandas as pd
from objetives import objetivo1, objetivo2, objetivo3


def evaluar_poblacion(
    poblacion: List[List[int]],
    df_jugadores: pd.DataFrame,
    df_sinergias: pd.DataFrame,
    distribucion_ideal:Dict[str, Dict[str, int]],
    
)-> List[Tuple[float, float, float]]:
    
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
