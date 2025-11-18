from src.grid import BogotaGrid
from src.route_optimizer import RouteOptimizer
from src.display import (
    display_welcome,
    display_establishments,
    display_origins,
    display_results
)


def main():
    display_welcome()
    grid = BogotaGrid()
    optimizer = RouteOptimizer(grid)
    
    display_establishments(grid)
    display_origins(grid)
    
    while True:
        print("\n" + "-"*70)
        destination = input("\nIngrese el nombre del establecimiento (o 'salir' para terminar): ").strip()
        
        if destination.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 ¡Hasta luego!")
            break
        
        results = optimizer.optimize_routes(destination)
        display_results(results)


if __name__ == "__main__":
    main()
