from typing import List, Tuple, Optional
from src.location import Location


class BogotaGrid:
    """Modelo de la cuadrícula de Bogotá con pesos variables por segmento"""
    
    def __init__(self):
        # Límites de la cuadrícula
        self.calle_min = 50
        self.calle_max = 55
        self.carrera_min = 10
        self.carrera_max = 15
        
        # Ubicaciones importantes
        self.javier_home = Location(54, 14)
        self.andreina_home = Location(52, 13)
        
        # Establecimientos
        self.establishments = {
            'The Darkness': Location(50, 14),
            'La Pasión': Location(54, 11),
            'Mi Rolita': Location(50, 12)
        }
    
    def get_travel_time(self, from_loc: Location, to_loc: Location) -> Optional[int]:
        """
        Calcula el tiempo de viaje entre dos ubicaciones adyacentes
        
        Args:
            from_loc: Ubicación de origen
            to_loc: Ubicación de destino
            
        Returns:
            Tiempo en minutos, o None si no son adyacentes
        """
        # Verificar que son adyacentes (solo movimiento horizontal o vertical)
        if from_loc.calle == to_loc.calle:
            # Movimiento horizontal ESTE-OESTE (a lo largo de una calle)
            if abs(from_loc.carrera - to_loc.carrera) != 1:
                return None
            
            # La calle que se está usando determina el tiempo
            calle = from_loc.calle
            
            # Calle 51 tiene mucha actividad comercial (10 minutos)
            if calle == 51:
                return 10
            else:
                return 5
                
        elif from_loc.carrera == to_loc.carrera:
            # Movimiento vertical NORTE-SUR (a lo largo de una carrera)
            if abs(from_loc.calle - to_loc.calle) != 1:
                return None
            
            # La carrera que se está usando determina el tiempo
            carrera = from_loc.carrera
            
            # Carreras 11, 12, 13 tienen aceras en mal estado (7 minutos)
            if carrera in [11, 12, 13]:
                return 7
            else:
                return 5
        else:
            # No son adyacentes
            return None
    
    def get_neighbors(self, location: Location) -> List[Tuple[Location, int]]:
        neighbors = []
        movements = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        
        for d_calle, d_carrera in movements:
            new_calle = location.calle + d_calle
            new_carrera = location.carrera + d_carrera
            
            if (self.calle_min <= new_calle <= self.calle_max and
                self.carrera_min <= new_carrera <= self.carrera_max):
                
                new_location = Location(new_calle, new_carrera)
                travel_time = self.get_travel_time(location, new_location)
                
                if travel_time is not None:
                    neighbors.append((new_location, travel_time))
        
        return neighbors
    
    def is_valid_location(self, location: Location) -> bool:
        return (self.calle_min <= location.calle <= self.calle_max and
                self.carrera_min <= location.carrera <= self.carrera_max)
    
    def is_location_occupied(self, location: Location) -> bool:
        """Verifica si una ubicación está ocupada por un establecimiento, Javier o Andreína"""
        # Verificar si es la casa de Javier o Andreína
        if location == self.javier_home or location == self.andreina_home:
            return True
        
        # Verificar si ya existe un establecimiento en esa ubicación
        for est_location in self.establishments.values():
            if est_location == location:
                return True
        
        return False
    
    def add_establishment(self, name: str, calle: int, carrera: int) -> bool:
        location = Location(calle, carrera)
        if not self.is_valid_location(location):
            return False
        if name in self.establishments:
            return False
        if self.is_location_occupied(location):
            return False
        self.establishments[name] = location
        return True
    
    def remove_establishment(self, name: str) -> bool:
        if name in self.establishments:
            del self.establishments[name]
            return True
        return False
