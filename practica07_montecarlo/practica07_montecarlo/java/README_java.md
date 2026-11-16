# Implementación en Java — Práctica 07

- Requiere JDK 17+ (probado con OpenJDK 21).
- `java.util.Random` con semilla fija 42; tamaños N = 1 000, 10 000, 100 000, 1 000 000.
- Tiempo con `System.nanoTime()` solo sobre generación + clasificación; mediana de 5 ejecuciones tras 5 pasadas de calentamiento (JIT).
- Imprime tabla en consola y exporta `../resultados/resultados_java.csv` (columnas: N, pi_estimado, error_absoluto, tiempo_s).

```bash
cd java
javac MonteCarlo.java
java MonteCarlo                 # ruta de CSV opcional: java MonteCarlo salida.csv
```
