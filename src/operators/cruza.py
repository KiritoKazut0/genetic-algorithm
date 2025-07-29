import random

def cruza_un_punto(equipo1, equipo2):
    punto_cruza = random.randint(1, len(equipo1) - 1)  # Entre 1 y 4 para equipos de 5
    hijo1 = equipo1[:punto_cruza] + [j for j in equipo2 if j not in equipo1[:punto_cruza]]
    hijo2 = equipo2[:punto_cruza] + [j for j in equipo1 if j not in equipo2[:punto_cruza]]
    
    # Aseguramos que los hijos tengan exactamente 5 jugadores
    hijo1 = hijo1[:5]
    hijo2 = hijo2[:5]
    
    return hijo1, hijo2


def cruza_poblacion(equipos):
    nueva_generacion = []
    
    if len(equipos) % 2 != 0:
        raise ValueError("La cantidad de equipos debe ser par para cruzarlos en pares.")
    
    for i in range(0, len(equipos), 2):
        padre1 = equipos[i]
        padre2 = equipos[i + 1]
        
        hijo1, hijo2 = cruza_un_punto(padre1, padre2)
        nueva_generacion.append(hijo1)
        nueva_generacion.append(hijo2)
    
    return nueva_generacion
