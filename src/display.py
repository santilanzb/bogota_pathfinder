from typing import List, Dict
from src.location import Location


def format_path(path: List[Location]) -> str:
    """
    Formatea un camino de manera legible
    
    Args:
        path: Lista de ubicaciones que forman el camino
        
    Returns:
        String formateado con el camino
    """
    if not path:
        return "  No hay ruta disponible"
    
    result = []
    for i, loc in enumerate(path):
        if i == 0:
            result.append(f"  Inicio: {loc}")
        elif i == len(path) - 1:
            result.append(f"  Destino: {loc}")
        else:
            result.append(f"  → {loc}")
    
    return "\n".join(result)


def display_results(results: Dict):
    """
    Muestra los resultados de manera formateada
    
    Args:
        results: Diccionario con los resultados del cálculo de rutas
    """
    if 'error' in results:
        print(f"\n❌ Error: {results['error']}")
        return
    
    print("\n" + "="*70)
    print(f"🎯 DESTINO: {results['destination']}")
    print(f"   Ubicación: {results['destination_location']}")
    print("="*70)
    
    # Información de Javier
    print("\n👨 JAVIER")
    print(f"   Origen: {results['javier']['path'][0]}")
    print(f"   Tiempo de caminata: {results['javier']['time']} minutos")
    print(f"   Cuadras a recorrer: {results['javier']['blocks']}")
    print("\n   Ruta:")
    print(format_path(results['javier']['path']))
    
    # Información de Andreína
    print("\n👩 ANDREÍNA")
    print(f"   Origen: {results['andreina']['path'][0]}")
    print(f"   Tiempo de caminata: {results['andreina']['time']} minutos")
    print(f"   Cuadras a recorrer: {results['andreina']['blocks']}")
    print("\n   Ruta:")
    print(format_path(results['andreina']['path']))
    
    # Sincronización
    print("\n" + "="*70)
    print("⏰ SINCRONIZACIÓN")
    print("="*70)
    
    sync = results['synchronization']
    
    if sync['first_to_leave'] == 'Ambos':
        print("✅ Ambos deben salir al mismo tiempo")
        print(f"   Tiempo total de viaje: {sync['total_time']} minutos")
    else:
        print(f"👉 {sync['first_to_leave']} debe salir primero")
        print(f"   Diferencia: {sync['time_difference']} minutos antes")
        print(f"   {sync['second_to_leave']} debe salir {sync['time_difference']} minutos después")
        print(f"   Tiempo total coordinado: {sync['total_time']} minutos")
    
    print("\n" + "="*70 + "\n")


def display_welcome():
    print("="*70)
    print("🏙️  BOGOTÁ PATHFINDER - Sistema de Rutas Óptimas")
    print("="*70)


def display_establishments(grid):
    print("\nEstablecimientos disponibles:")
    for i, (name, location) in enumerate(grid.establishments.items(), 1):
        print(f"  {i}. {name} - {location}")


def display_origins(grid):
    print("\nUbicaciones de origen:")
    print(f"  - Javier: {grid.javier_home}")
    print(f"  - Andreína: {grid.andreina_home}")
