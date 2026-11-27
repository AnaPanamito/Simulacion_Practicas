# Práctica 06 – Simulación (UNL) – Versión Python

Validación estadística de números pseudoaleatorios (LCG) con Chi-cuadrado y Kolmogorov-Smirnov, más estimación de π por Monte Carlo.

## Contenido
| Archivo | Descripción |
|---|---|
| `practica06.py` | Programa completo (LCG, Chi-cuadrado, KS, estimación de π, gráficos KS). |
| `salida_python.txt` | Salida de referencia (determinista) obtenida al ejecutar el programa. |
| `tiempos_python.csv` | Tiempos de referencia medidos (dependen de la máquina). |
| `ks_A.png` … `ks_D.png` | Gráficos F_n(x) empírica vs. F(x)=x teórica, una por configuración. |

## Requisitos
- Python 3.8 o superior.
- Matplotlib (**opcional**, solo para los gráficos; sin él el programa funciona igual).
- No usa NumPy, Pandas ni SciPy: los valores p están implementados en el propio código.

## Ejecución
```
python3 practica06.py            # Linux / macOS
python practica06.py             # Windows
```
Para guardar la salida y compararla con la de Java:
```
python3 practica06.py > salida_python.txt
```
Los tiempos se muestran por la salida de error (stderr) y se guardan en `tiempos_python.csv`. Los gráficos se guardan como `ks_A.png`, `ks_B.png`, `ks_C.png` y `ks_D.png`.

## Parámetros usados (propuestos; la guía no los especifica)
| Config. | X0 | a | c | m |
|---|---|---|---|---|
| A (principal) | 12345 | 1664525 | 1013904223 | 2^32 |
| B (ANSI C) | 12345 | 1103515245 | 12345 | 2^31 |
| C (RANDU) | 1 | 65539 | 0 | 2^31 |
| D (período corto) | 12345 | 137 | 187 | 256 |

Pruebas con N = 10 000 y k = 10 intervalos (gl = 9), α = 0,05. La tabla de π usa la configuración A con N = 1 000; 10 000; 100 000 y 1 000 000 puntos (cada punto usa 2 números consecutivos del LCG).

## Resultados esperados (resumen)
- Config. A: χ² = 14,1600, gl = 9, p = 0,116746 → no se rechaza H0; KS: D = 0,005960, p = 0,868567 → no se rechaza H0.
- π (config. A): 3,1720000000 (N=1000), 3,1588000000 (10 000), 3,1410800000 (100 000), 3,1426560000 (1 000 000).
- Primer número generado (config. A): 0,0204026857.

La salida completa está en `salida_python.txt`. Todo excepto los tiempos debe coincidir exactamente en tu equipo.

## Cómo comprobar que Python y Java generan lo mismo
1. Ejecuta este programa y redirige la salida a `salida_python.txt`.
2. Ejecuta la versión Java y redirige la salida a `salida_java.txt`.
3. Compara:
```
diff salida_python.txt salida_java.txt      # Linux / macOS
fc salida_python.txt salida_java.txt        # Windows
```
No debe haber diferencias (los tiempos no se imprimen en stdout, por eso no interfieren).

## Notas
- Los tiempos son la mediana de 5 repeticiones en milisegundos y dependen del equipo; anota tu hardware al reportarlos.
- El gráfico KS solo lo genera la versión Python.
