import heapq
from typing import List, Tuple, Dict
from src.location import Location
from src.grid import BogotaGrid


class PathFinder:
    """Implementa el algoritmo de Dijkstra para encontrar caminos óptimos"""
    
    def __init__(self, grid: BogotaGrid):
        """
        Inicializa el PathFinder con una cuadrícula
        
        Args:
            grid: Instancia de BogotaGrid
        """
        self.grid = grid
    
    def find_shortest_path(self, start: Location, end: Location) -> Tuple[List[Location], int]:
        """
        Encuentra el camino más corto usando el algoritmo de Dijkstra
        
        Args:
            start: Ubicación de inicio
            end: Ubicación de destino
            
        Returns:
            Tupla con (lista de ubicaciones en el camino, tiempo total en minutos)
        """
        # Priority queue: (tiempo_acumulado, ubicación)
        pq = [(0, start)]
        
        # Diccionarios para tracking
        distances: Dict[Location, int] = {start: 0}
        previous: Dict[Location, Location] = {start: None}
        visited = set()
        
        while pq:
            current_time, current_loc = heapq.heappop(pq)
            
            if current_loc in visited:
                continue
            
            visited.add(current_loc)
            
            # Si llegamos al destino, reconstruir el camino
            if current_loc == end:
                path = self._reconstruct_path(previous, end)
                return path, current_time
            
            # Explorar vecinos
            for neighbor, travel_time in self.grid.get_neighbors(current_loc):
                if neighbor in visited:
                    continue
                
                new_time = current_time + travel_time
                
                if neighbor not in distances or new_time < distances[neighbor]:
                    distances[neighbor] = new_time
                    previous[neighbor] = current_loc
                    heapq.heappush(pq, (new_time, neighbor))
        
        # No se encontró camino
        return [], float('inf')
    
    def _reconstruct_path(self, previous: Dict[Location, Location], end: Location) -> List[Location]:
        path = []
        loc = end
        while loc is not None:
            path.append(loc)
            loc = previous.get(loc)
        path.reverse()
        return path
