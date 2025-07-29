
def calcular_fitnes_general(
    rendimiento: float,
    sinergia: float,
    promedio_roles: float
) -> float:
    
    peso_rendimiento = 0.4
    peso_sinergia = 0.3
    peso_roles = 0.3
    
    fitnes_general = (
        peso_rendimiento * rendimiento +
        peso_sinergia * sinergia +
        peso_roles * promedio_roles
    )
    
    return fitnes_general