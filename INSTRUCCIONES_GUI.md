# Instrucciones de Uso - Interfaz Gráfica

## Inicio Rápido

1. **Ejecutar el programa:**
   ```bash
   python main_gui.py
   ```

2. **Usar la interfaz:**
   - Selecciona un establecimiento usando los botones de radio
   - Haz clic en "🔍 Calcular Rutas Óptimas"
   - Observa el grafo visualizado con las rutas
   - Lee los resultados en el panel izquierdo

## Características de la Visualización

### Panel Izquierdo (Controles y Resultados)

**📍 Ubicaciones de Origen**
- Muestra las casas de Javier y Andreína

**🎯 Seleccionar Destino**
- Radio buttons para cada establecimiento
- Muestra la ubicación de cada uno

**🔍 Botón Calcular**
- Ejecuta el algoritmo de Dijkstra
- Actualiza el grafo automáticamente

**📊 Resultados**
- **Destino**: Establecimiento seleccionado
- **Javier** (azul): Tiempo y número de cuadras
- **Andreína** (rojo): Tiempo y número de cuadras
- **Sincronización**: Quién sale primero y cuántos minutos antes

### Panel Derecho (Visualización del Grafo)

**Elementos del Grafo:**

1. **Cuadrícula Base**
   - Líneas grises: Calles y carreras normales (5 min)
   - Líneas rojas gruesas: Zonas especiales

2. **Zonas Especiales**
   - Fondo rojo claro en Calle 51 (10 min)
   - Fondo rojo claro en Carreras 11, 12, 13 (7 min)

3. **Marcadores**
   - 🔵 Círculo azul: Casa de Javier
   - 🔴 Círculo rojo: Casa de Andreína
   - 🟡 Cuadrados naranjas: Establecimientos
   - ⭐ Estrella amarilla: Destino seleccionado

4. **Rutas Calculadas**
   - Línea azul gruesa: Ruta de Javier
   - Línea roja gruesa: Ruta de Andreína
   - Puntos: Cada intersección del camino

5. **Leyenda**
   - Muestra el tiempo total de cada ruta
   - Ubicada en la esquina superior izquierda

## Colores y Símbolos

| Color/Símbolo | Significado |
|---------------|-------------|
| 🔵 Azul | Javier y su ruta |
| 🔴 Rojo | Andreína y su ruta |
| 🟡 Naranja | Establecimientos |
| ⭐ Amarillo | Destino actual |
| 🟥 Rojo claro | Zonas con tiempo mayor |
| ⚪ Gris | Cuadrícula normal |

## Ejemplo de Uso

### Paso a Paso: Calcular ruta a "The Darkness"

1. Abre la aplicación: `python main_gui.py`
2. En el panel izquierdo, selecciona "The Darkness"
3. Haz clic en "🔍 Calcular Rutas Óptimas"
4. Observa:
   - Ruta azul: Camino de Javier
   - Ruta roja: Camino de Andreína
   - Estrella amarilla en el destino
5. Lee en el panel de resultados:
   - Javier: 25 minutos
   - Andreína: 22 minutos
   - Javier debe salir 3 minutos antes

## Interpretación de Resultados

### Sincronización

**Si dice "Ambos salen al mismo tiempo":**
- Los tiempos son iguales
- Pueden salir juntos

**Si dice "X debe salir primero":**
- La persona mencionada tiene un camino más largo
- Debe salir N minutos antes
- Así llegan simultáneamente

### Tiempos

Los tiempos mostrados incluyen:
- Cuadras normales: 5 min cada una
- Carreras 11, 12, 13: 7 min cada cuadra
- Calle 51: 10 min cada cuadra

## Comparación: GUI vs Terminal

### Ventajas de la GUI:
✅ Visualización inmediata del grafo
✅ Colores que facilitan la interpretación
✅ No necesitas escribir nombres exactos
✅ Ves todas las opciones disponibles
✅ Interfaz más intuitiva

### Ventajas del Terminal:
✅ Más rápido si conoces los nombres
✅ Menor uso de recursos
✅ Útil para scripting

## Requisitos

- Python 3.7 o superior
- tkinter (incluido con Python)
- matplotlib (instalar con: `pip install matplotlib`)

## Solución de Problemas

### La ventana no aparece
- Verifica que tkinter esté instalado
- En Linux: `sudo apt-get install python3-tk`

### Error con matplotlib
- Instala matplotlib: `pip install matplotlib`

### Ventana muy pequeña o muy grande
- Tamaño por defecto: 1400x800
- Puedes redimensionar la ventana manualmente

### Los emojis no se ven bien
- Normal en algunos sistemas
- La funcionalidad no se ve afectada

## Tips

1. **Prueba todas las rutas**: Selecciona cada establecimiento para ver cómo cambian las rutas
2. **Observa las zonas especiales**: Nota cómo las rutas evitan o usan las zonas rojas
3. **Compara tiempos**: Fíjate cómo las rutas más cortas no siempre son las más rápidas
4. **Redimensiona**: Puedes agrandar la ventana para ver mejor el grafo
