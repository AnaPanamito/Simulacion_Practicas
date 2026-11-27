# Práctica Nro. 05 – Generador Congruencial Lineal (LCG) en Python y Java

**Asignatura:** Simulación · **Unidad 2:** Generación de números pseudoaleatorios
**Carrera de Computación – FEIRNNR, UNL**

## Descripción
Implementación del Generador Congruencial Lineal

    X(n+1) = (a · X(n) + c) mod m        U(n) = X(n) / m

con los parámetros de *Numerical Recipes*:

| Parámetro | Valor |
|---|---|
| a | 1 664 525 |
| c | 1 013 904 223 |
| m | 2³² = 4 294 967 296 |
| Semilla X₀ | 12345 |
| Cantidad de valores | 10 000 |

## Contenido de la carpeta
| Archivo | Descripción |
|---|---|
| `lcg.py` | LCG en Python: imprime las 20 primeras observaciones, genera `lcg_python.csv` y la gráfica `lcg_grafica.png` |
| `LCG.java` | LCG en Java (`long` + máscara `0xFFFFFFFFL`): imprime 20 observaciones, genera `lcg_java.csv` y calcula el período |
| `extras.py` | Cambio de semilla, condiciones de Hull–Dobell, períodos con m pequeño, parámetros inadecuados y pruebas básicas (media, varianza, χ², autocorrelación) |
| `lcg_python.csv`, `lcg_java.csv` | Secuencias generadas (n, Xn, Un); idénticas entre sí |
| `lcg_grafica.png` | Gráfica: Un vs n, histograma y diagrama (Un, Un+1) |

## Requisitos
- Python 3 con `matplotlib` (`pip install matplotlib`)
- JDK 11 o superior (para `javac` y `java`)
- Linux o macOS

## Ejecución
```bash
# Python
pip install matplotlib
python3 lcg.py
python3 extras.py

# Java
javac LCG.java
java LCG          # el cálculo de períodos tarda unos segundos
```

## Verificar que Python y Java coinciden
```bash
tr -d '\r' < lcg_python.csv > py.csv
cmp py.csv lcg_java.csv && echo "Secuencias identicas"
```

## Resultados principales
- Las primeras 20 observaciones coinciden en Python y Java; los CSV de 10 000 filas son idénticos.
- Hull–Dobell se cumple (c impar, a ≡ 1 mod 4) → período teórico 2³².
- Período observado: **4 294 967 296** para las semillas 12345, 1 y 987654321.
- Media 0.4987, varianza 0.0830, χ² = 14.17 (< 16.92), autocorrelación lag-1 = −0.015.

## Notas
- X₀ es la semilla y se lista como n = 0.
- Si ejecutas los programas, los CSV y la gráfica se sobrescriben.
