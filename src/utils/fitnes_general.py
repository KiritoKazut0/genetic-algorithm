from typing import Dict

def calcular_fitnes_general(
    rendimiento: float,
    sinergia: float,
    promedio_roles: float,
    peso_fitnes: Dict[str, float]
) -> float:
    
    peso_rendimiento = peso_fitnes.get("rendimiento", 0.4)
    peso_sinergia = peso_fitnes.get("sinergia", 0.3)
    peso_roles = peso_fitnes.get("balance_roles", 0.3)
    
    fitnes_general = (
        peso_rendimiento * rendimiento +
        peso_sinergia * sinergia +
        peso_roles * promedio_roles
    )
    
    return fitnes_general