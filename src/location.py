from dataclasses import dataclass


@dataclass
class Location:
    calle: int
    carrera: int
    
    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return self.calle == other.calle and self.carrera == other.carrera
    
    def __lt__(self, other):
        if not isinstance(other, Location):
            return NotImplemented
        return (self.calle, self.carrera) < (other.calle, other.carrera)
    
    def __hash__(self):
        return hash((self.calle, self.carrera))
    
    def __repr__(self):
        return f"Calle {self.calle} con Carrera {self.carrera}"
    
    def __str__(self):
        return self.__repr__()
