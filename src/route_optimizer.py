from typing import Dict
from src.grid import BogotaGrid
from src.pathfinder import PathFinder


class RouteOptimizer:
    """Optimiza las rutas para que Javier y Andreína lleguen simultáneamente"""
    
    def __init__(self, grid: BogotaGrid):
        """
        Inicializa el optimizador de rutas
        
        Args:
            grid: Instancia de BogotaGrid
        """
        self.grid = grid
        self.pathfinder = PathFinder(grid)
    
    def optimize_routes(self, destination_name: str) -> Dict:
        """
        Calcula las rutas óptimas para Javier y Andreína
        
        Args:
            destination_name: Nombre del establecimiento destino
            
        Returns:
            Diccionario con toda la información de las rutas y sincronización
        """
        if destination_name not in self.grid.establishments:
            return {'error': f'Establecimiento "{destination_name}" no encontrado'}
        
        destination = self.grid.establishments[destination_name]
        
        # Calcular rutas óptimas para cada persona
        javier_path, javier_time = self.pathfinder.find_shortest_path(
            self.grid.javier_home, destination
        )
        
        andreina_path, andreina_time = self.pathfinder.find_shortest_path(
            self.grid.andreina_home, destination
        )
        
        # Validar que existen rutas
        if not javier_path or not andreina_path:
            return {'error': 'No se pudo encontrar una ruta válida'}
        
        # Calcular información de sincronización
        sync_info = self._calculate_synchronization(javier_time, andreina_time)
        
        return {
            'destination': destination_name,
            'destination_location': destination,
            'javier': {
                'path': javier_path,
                'time': javier_time,
                'blocks': len(javier_path) - 1
            },
            'andreina': {
                'path': andreina_path,
                'time': andreina_time,
                'blocks': len(andreina_path) - 1
            },
            'synchronization': sync_info
        }
    
    def _calculate_synchronization(self, javier_time: int, andreina_time: int) -> Dict:
        time_difference = abs(javier_time - andreina_time)
        
        if javier_time > andreina_time:
            first_to_leave = 'Javier'
            second_to_leave = 'Andreína'
        elif andreina_time > javier_time:
            first_to_leave = 'Andreína'
            second_to_leave = 'Javier'
        else:
            first_to_leave = 'Ambos'
            second_to_leave = None
        
        return {
            'first_to_leave': first_to_leave,
            'second_to_leave': second_to_leave,
            'time_difference': time_difference,
            'total_time': max(javier_time, andreina_time)
        }
