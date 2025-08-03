import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GraficaEvolucion:
    def __init__(self):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.lineas = {
            'mejor': self.ax.plot([], [], 'g-', label='Mejor')[0],
            'promedio': self.ax.plot([], [], 'b-', label='Promedio')[0],
            'peor': self.ax.plot([], [], 'r-', label='Peor')[0]
        }
        self.configurar_grafica()
        self.x_data = []
        self.y_data = {k: [] for k in self.lineas}
    
    def configurar_grafica(self):
        self.ax.set_title('Evolución del Fitness')
        self.ax.set_xlabel('Generación')
        self.ax.set_ylabel('Fitness')
        self.ax.legend()
        self.ax.grid(True)
    
    def actualizar(self, generacion, mejor, promedio, peor):
        self.x_data.append(generacion)
        self.y_data['mejor'].append(mejor)
        self.y_data['promedio'].append(promedio)
        self.y_data['peor'].append(peor)
        
        for key, linea in self.lineas.items():
            linea.set_data(self.x_data, self.y_data[key])
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def guardar(self, filename):
        plt.savefig(filename)
        plt.close()

def mostrar_evolucion_tiempo_real():
    return GraficaEvolucion()