import csv
import random

# Configuración
random.seed(42)  # Para resultados reproducibles
NUM_JUGADORES = 200

# Generar todas las combinaciones únicas (A < B) con sinergias aleatorias
with open('sinergias_solo_ids.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['jugador_A', 'jugador_B', 'sinergia'])
    
    for i in range(1, NUM_JUGADORES + 1):
        for j in range(i + 1, NUM_JUGADORES + 1):
            sinergia = random.randint(0, 100)  # Rango 0-100
            writer.writerow([i, j, sinergia])

print(f"¡Archivo generado con {NUM_JUGADORES} jugadores y {NUM_JUGADORES * (NUM_JUGADORES - 1) // 2} pares únicos!")