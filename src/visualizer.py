import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from typing import List, Dict
from src.location import Location
from src.grid import BogotaGrid


class GridVisualizer:
    
    def __init__(self, grid: BogotaGrid):
        self.grid = grid
        
    def create_figure(self, results: Dict = None):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Configurar límites y etiquetas
        # Invertir eje X: carreras crecen de este (10) a oeste (15)
        ax.set_xlim(self.grid.carrera_max + 0.5, self.grid.carrera_min - 0.5)
        ax.set_ylim(self.grid.calle_min - 0.5, self.grid.calle_max + 0.5)
        ax.set_xlabel('Carrera (10=Este, 15=Oeste)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Calle (aumenta hacia el Norte)', fontsize=12, fontweight='bold')
        ax.set_title('Cuadrícula de Bogotá - Rutas Óptimas', fontsize=14, fontweight='bold')
        
        # Grilla
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xticks(range(self.grid.carrera_min, self.grid.carrera_max + 1))
        ax.set_yticks(range(self.grid.calle_min, self.grid.calle_max + 1))
        
        # Dibujar todas las conexiones de la cuadrícula
        self._draw_grid_connections(ax)
        
        # Marcar zonas especiales
        self._mark_special_zones(ax)
        
        # Marcar ubicaciones importantes
        self._mark_locations(ax)
        
        # Si hay resultados, dibujar las rutas
        if results and 'error' not in results:
            self._draw_routes(ax, results)
        
        plt.tight_layout()
        return fig
    
    def _draw_grid_connections(self, ax):
        # Dibujar líneas horizontales (calles)
        for calle in range(self.grid.calle_min, self.grid.calle_max + 1):
            for carrera in range(self.grid.carrera_min, self.grid.carrera_max):
                color = '#ff6b6b' if calle == 51 else '#95a5a6'
                width = 2 if calle == 51 else 0.5
                ax.plot([carrera, carrera + 1], [calle, calle], 
                       color=color, linewidth=width, alpha=0.3, zorder=1)
        
        # Dibujar líneas verticales (carreras)
        for carrera in range(self.grid.carrera_min, self.grid.carrera_max + 1):
            for calle in range(self.grid.calle_min, self.grid.calle_max):
                color = '#ff6b6b' if carrera in [11, 12, 13] else '#95a5a6'
                width = 2 if carrera in [11, 12, 13] else 0.5
                ax.plot([carrera, carrera], [calle, calle + 1], 
                       color=color, linewidth=width, alpha=0.3, zorder=1)
    
    def _mark_special_zones(self, ax):
        # Marcar Calle 51 (10 min)
        rect = patches.Rectangle((self.grid.carrera_min - 0.4, 51 - 0.1), 
                                 self.grid.carrera_max - self.grid.carrera_min + 0.8, 0.2,
                                 linewidth=0, facecolor='#ff6b6b', alpha=0.15, zorder=0)
        ax.add_patch(rect)
        ax.text(self.grid.carrera_max + 0.3, 51, '10 min', fontsize=8, 
               color='#c0392b', fontweight='bold', va='center')
        
        # Marcar Carreras 11, 12, 13 (7 min)
        for carrera in [11, 12, 13]:
            rect = patches.Rectangle((carrera - 0.1, self.grid.calle_min - 0.4), 
                                     0.2, self.grid.calle_max - self.grid.calle_min + 0.8,
                                     linewidth=0, facecolor='#ff6b6b', alpha=0.15, zorder=0)
            ax.add_patch(rect)
            ax.text(carrera, self.grid.calle_max + 0.3, '7 min', fontsize=8, 
                   color='#c0392b', fontweight='bold', ha='center')
    
    def _mark_locations(self, ax):
        # Casa de Javier
        ax.plot(self.grid.javier_home.carrera, self.grid.javier_home.calle, 
               'o', markersize=15, color='#3498db', markeredgecolor='black', 
               markeredgewidth=2, label='Javier', zorder=5)
        ax.text(self.grid.javier_home.carrera + 0.3, self.grid.javier_home.calle, 
               'Javier', fontsize=9, fontweight='bold', color='#2c3e50')
        
        # Casa de Andreína
        ax.plot(self.grid.andreina_home.carrera, self.grid.andreina_home.calle, 
               'o', markersize=15, color='#e74c3c', markeredgecolor='black', 
               markeredgewidth=2, label='Andreína', zorder=5)
        ax.text(self.grid.andreina_home.carrera + 0.3, self.grid.andreina_home.calle, 
               'Andreína', fontsize=9, fontweight='bold', color='#2c3e50')
        
        # Establecimientos
        for name, loc in self.grid.establishments.items():
            ax.plot(loc.carrera, loc.calle, 's', markersize=12, 
                   color='#f39c12', markeredgecolor='black', 
                   markeredgewidth=2, zorder=5)
            ax.text(loc.carrera, loc.calle - 0.3, name, 
                   fontsize=8, ha='center', fontweight='bold', color='#2c3e50')
    
    def _draw_routes(self, ax, results):
        # Ruta de Javier (azul)
        javier_path = results['javier']['path']
        if len(javier_path) > 1:
            carreras = [loc.carrera for loc in javier_path]
            calles = [loc.calle for loc in javier_path]
            ax.plot(carreras, calles, 'o-', color='#3498db', linewidth=4, 
                   markersize=8, alpha=0.7, label=f"Javier ({results['javier']['time']} min)", 
                   zorder=3)
        
        # Ruta de Andreína (rojo)
        andreina_path = results['andreina']['path']
        if len(andreina_path) > 1:
            carreras = [loc.carrera for loc in andreina_path]
            calles = [loc.calle for loc in andreina_path]
            ax.plot(carreras, calles, 'o-', color='#e74c3c', linewidth=4, 
                   markersize=8, alpha=0.7, label=f"Andreína ({results['andreina']['time']} min)", 
                   zorder=4)
        
        # Marcar destino
        dest = results['destination_location']
        ax.plot(dest.carrera, dest.calle, '*', markersize=25, 
               color='#f1c40f', markeredgecolor='black', 
               markeredgewidth=2, label='Destino', zorder=6)
        
        ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
