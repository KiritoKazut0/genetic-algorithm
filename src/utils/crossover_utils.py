

def reparar_con_diferencia(hijo, padre):
    vistos = set()
    duplicados_indices = []

    for i, gen in enumerate(hijo):
        if gen in vistos:
            duplicados_indices.append(i)
        else:
            vistos.add(gen)
    faltantes = [g for g in padre if g not in vistos]

    for i in duplicados_indices:
        hijo[i] = faltantes.pop(0)
    
    return hijo
