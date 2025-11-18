# Bogotá Pathfinder

Sistema de navegación y optimización de rutas para Javier y Andreína en la cuadrícula de Bogotá.

## Descripción

Este programa encuentra las rutas óptimas para que dos personas lleguen simultáneamente a un establecimiento, considerando diferentes tiempos de viaje según las calles y carreras de la ciudad.

## Características

- **Algoritmo de Dijkstra**: Encuentra el camino más corto considerando pesos variables
- **Sincronización automática**: Calcula quién debe salir primero y cuándo
- **Modular**: Arquitectura limpia con separación de responsabilidades
- **Extensible**: Fácil agregar nuevos establecimientos o modificar la cuadrícula

## Estructura del Proyecto

```
bogota_pathfinder/
│
├── src/
│   ├── __init__.py           # Inicializador del paquete
│   ├── location.py           # Clase Location (ubicaciones)
│   ├── grid.py               # Clase BogotaGrid (modelo de la cuadrícula)
│   ├── pathfinder.py         # Clase PathFinder (algoritmo de Dijkstra)
│   ├── route_optimizer.py    # Clase RouteOptimizer (optimización de rutas)
│   └── display.py            # Funciones de visualización
│
├── main.py                   # Punto de entrada principal
└── README.md                 # Este archivo
```

## Reglas de la Cuadrícula

### Límites
- **Calles**: 50 a 55 (van oeste-este)
- **Carreras**: 10 a 15 (van norte-sur)

### Tiempos de Viaje
- **Cuadras normales**: 5 minutos
- **Carreras 11, 12, 13** (aceras en mal estado): 7 minutos
- **Calle 51** (actividad comercial): 10 minutos

### Ubicaciones

**Hogares:**
- Javier: Calle 54 con Carrera 14
- Andreína: Calle 52 con Carrera 13

**Establecimientos:**
1. **The Darkness**: Calle 50 con Carrera 14
2. **La Pasión**: Calle 54 con Carrera 11
3. **Mi Rolita**: Calle 50 con Carrera 12

## Uso

### Ejecutar el programa

```bash
python main.py
```

### Ejemplo de Interacción

```
Ingrese el nombre del establecimiento: The Darkness

🎯 DESTINO: The Darkness
   Ubicación: Calle 50 con Carrera 14

👨 JAVIER
   Origen: Calle 54 con Carrera 14
   Tiempo de caminata: 20 minutos
   ...

👩 ANDREÍNA
   Origen: Calle 52 con Carrera 13
   Tiempo de caminata: 17 minutos
   ...

⏰ SINCRONIZACIÓN
   👉 Javier debe salir primero
   Diferencia: 3 minutos antes
```

## Módulos

### `location.py`
Define la clase `Location` que representa una intersección en la cuadrícula.

### `grid.py`
Contiene `BogotaGrid` que modela la cuadrícula con:
- Límites de la zona
- Ubicaciones importantes
- Cálculo de tiempos de viaje
- Vecinos adyacentes

### `pathfinder.py`
Implementa `PathFinder` con el algoritmo de Dijkstra para encontrar caminos óptimos.

### `route_optimizer.py`
`RouteOptimizer` coordina las rutas de ambas personas y calcula la sincronización.

### `display.py`
Funciones de formateo y visualización de resultados.

## Extensibilidad

### Agregar nuevos establecimientos

Edita `src/grid.py`:

```python
self.establishments = {
    'The Darkness': Location(50, 14),
    'La Pasión': Location(54, 11),
    'Mi Rolita': Location(50, 12),
    'Nuevo Bar': Location(53, 12)  # Agregar aquí
}
```

### Modificar tiempos de viaje

Edita el método `get_travel_time()` en `src/grid.py`.

### Cambiar límites de la cuadrícula

Modifica las constantes en `__init__()` de `BogotaGrid`.

## Requisitos

- Python 3.7+
- No requiere dependencias externas (solo biblioteca estándar)

## Autor

Sistema desarrollado para resolver el problema de optimización de rutas en Bogotá.
