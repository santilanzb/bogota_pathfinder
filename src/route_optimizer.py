from typing import Dict, Set, Tuple
from src.grid import BogotaGrid
from src.pathfinder import PathFinder
from src.location import Location


class RouteOptimizer:
    
    def __init__(self, grid: BogotaGrid):
        self.grid = grid
        self.pathfinder = PathFinder(grid)
    
    def optimize_routes(self, destination_name: str) -> Dict:
        if destination_name not in self.grid.establishments:
            return {'error': f'Establecimiento "{destination_name}" no encontrado'}
        
        destination = self.grid.establishments[destination_name]
        
        # Calcular primera ruta para Javier (sin restricciones)
        javier_path, javier_time = self.pathfinder.find_shortest_path(
            self.grid.javier_home, destination
        )
        
        if not javier_path:
            return {'error': 'No se pudo encontrar una ruta válida para Javier'}
        
        # Extraer las aristas (cuadras) que usa Javier
        javier_edges = self._get_path_edges(javier_path)
        
        # Calcular ruta para Andreína evitando las cuadras de Javier
        andreina_path, andreina_time = self.pathfinder.find_shortest_path(
            self.grid.andreina_home, destination, blocked_edges=javier_edges
        )
        
        # Si Andreína no puede llegar evitando a Javier, intentar al revés
        if not andreina_path:
            andreina_path, andreina_time = self.pathfinder.find_shortest_path(
                self.grid.andreina_home, destination
            )
            
            if not andreina_path:
                return {'error': 'No se pudo encontrar una ruta válida'}
            
            andreina_edges = self._get_path_edges(andreina_path)
            javier_path, javier_time = self.pathfinder.find_shortest_path(
                self.grid.javier_home, destination, blocked_edges=andreina_edges
            )
            
            if not javier_path:
                return {'error': 'No se pudieron encontrar rutas sin cruces'}
        
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
    
    def _get_path_edges(self, path: list) -> Set[Tuple[Location, Location]]:
        edges = set()
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            edges.add(edge)
        return edges
    
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
