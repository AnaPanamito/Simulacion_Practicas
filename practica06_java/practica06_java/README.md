# Práctica 06 – Simulación (UNL) – Versión Java

Validación estadística de números pseudoaleatorios (LCG) con Chi-cuadrado y Kolmogorov-Smirnov, más estimación de π por Monte Carlo.

## Contenido
| Archivo | Descripción |
|---|---|
| `Practica06.java` | Programa completo en un solo archivo (LCG, Chi-cuadrado, KS, estimación de π). |
| `salida_java.txt` | Salida de referencia (determinista) obtenida al ejecutar el programa. |
| `tiempos_java.csv` | Tiempos de referencia medidos (dependen de la máquina). |

## Requisitos
- JDK 11 o superior (probado con OpenJDK 21).
- Sin dependencias externas ni IDE obligatorio (también funciona en IntelliJ IDEA, Eclipse o NetBeans).

## Ejecución
Opción 1, sin compilar (JDK 11+):
```
java Practica06.java
```
Opción 2, compilando:
```
javac Practica06.java
java Practica06
```
Para guardar la salida y compararla con la de Python:
```
java Practica06.java > salida_java.txt
```
Los tiempos se muestran por la salida de error (stderr) y se guardan en `tiempos_java.csv`. El programa fuerza UTF-8 en la salida estándar para que las tildes sean iguales a las de Python.

## Parámetros usados (propuestos; la guía no los especifica)
| Config. | X0 | a | c | m |
|---|---|---|---|---|
| A (principal) | 12345 | 1664525 | 1013904223 | 2^32 |
| B (ANSI C) | 12345 | 1103515245 | 12345 | 2^31 |
| C (RANDU) | 1 | 65539 | 0 | 2^31 |
| D (período corto) | 12345 | 137 | 187 | 256 |

Se usa aritmética `long`: el producto a·X no desborda (el mayor es ≈ 2,4·10^18 < 9,2·10^18). Pruebas con N = 10 000 y k = 10 intervalos (gl = 9), α = 0,05. La tabla de π usa la configuración A con N = 1 000; 10 000; 100 000 y 1 000 000 puntos (cada punto usa 2 números consecutivos del LCG).

## Resultados esperados (resumen)
- Config. A: χ² = 14,1600, gl = 9, p = 0,116746 → no se rechaza H0; KS: D = 0,005960, p = 0,868567 → no se rechaza H0.
- π (config. A): 3,1720000000 (N=1000), 3,1588000000 (10 000), 3,1410800000 (100 000), 3,1426560000 (1 000 000).
- Primer número generado (config. A): 0,0204026857.

La salida completa está en `salida_java.txt`. Todo excepto los tiempos debe coincidir exactamente en tu equipo.

## Cómo comprobar que Java y Python generan lo mismo
1. Ejecuta este programa y redirige la salida a `salida_java.txt`.
2. Ejecuta la versión Python y redirige la salida a `salida_python.txt`.
3. Compara:
```
diff salida_python.txt salida_java.txt      # Linux / macOS
fc salida_python.txt salida_java.txt        # Windows
```
No debe haber diferencias (los tiempos no se imprimen en stdout, por eso no interfieren).

## Notas
- Los tiempos son la mediana de 5 repeticiones en milisegundos; en N pequeños influye el calentamiento del JIT. Dependen del equipo; anota tu hardware al reportarlos.
- Esta versión no genera gráficos (Java sin bibliotecas externas no grafica); los gráficos KS los produce la versión Python.
