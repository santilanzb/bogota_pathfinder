import heapq
from typing import List, Tuple, Dict, Set
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
    
    def find_shortest_path(self, start: Location, end: Location, blocked_edges: Set[Tuple[Location, Location]] = None) -> Tuple[List[Location], int]:
        if blocked_edges is None:
            blocked_edges = set()
        
        pq = [(0, start)]
        distances: Dict[Location, int] = {start: 0}
        previous: Dict[Location, Location] = {start: None}
        visited = set()
        
        while pq:
            current_time, current_loc = heapq.heappop(pq)
            
            if current_loc in visited:
                continue
            
            visited.add(current_loc)
            
            if current_loc == end:
                path = self._reconstruct_path(previous, end)
                return path, current_time
            
            for neighbor, travel_time in self.grid.get_neighbors(current_loc):
                if neighbor in visited:
                    continue
                
                # Verificar si esta arista está bloqueada (Javier y Andreína no pueden caminar juntos)
                edge = (current_loc, neighbor)
                edge_reverse = (neighbor, current_loc)
                if edge in blocked_edges or edge_reverse in blocked_edges:
                    continue
                
                new_time = current_time + travel_time
                
                if neighbor not in distances or new_time < distances[neighbor]:
                    distances[neighbor] = new_time
                    previous[neighbor] = current_loc
                    heapq.heappush(pq, (new_time, neighbor))
        
        return [], float('inf')
    
    def _reconstruct_path(self, previous: Dict[Location, Location], end: Location) -> List[Location]:
        path = []
        loc = end
        while loc is not None:
            path.append(loc)
            loc = previous.get(loc)
        path.reverse()
        return path
