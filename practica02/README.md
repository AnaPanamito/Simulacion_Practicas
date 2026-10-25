# Práctica 02: Comparación de modelos determinísticos, estocásticos, discretos y continuos

**Asignatura:** Simulación (Ciclo 5) · **Carrera de Computación, UNL**
**Sistema de estudio:** crecimiento poblacional · **Datos:** `[1000, 1100, 1250, 1400, 1600, 1850, 2100]`

## Archivos

| Archivo | Descripción |
|---|---|
| `practica02.py` | Implementa los 4 modelos, estima parámetros, calcula errores y genera las gráficas. |
| `salida_consola.txt` | Resultados impresos por el script (semilla 42). |
| `grafica_1_comparacion_modelos.png` | Los 4 modelos frente a los datos reales. |
| `grafica_2_influencia_r.png` | Influencia de r (crecimiento, constante y decrecimiento). |
| `grafica_3_efecto_sigma.png` | Efecto del nivel de ruido σ. |
| `grafica_4_montecarlo.png` | 500 simulaciones del modelo estocástico. |
| `grafica_5_efecto_dt.png` | Efecto del paso dt en Euler. |
| `grafica_6_nuevo_arreglo.png` | Simulación con un nuevo arreglo de datos (r < 0). |

## Cómo ejecutar

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/macOS: source venv/bin/activate)
pip install numpy matplotlib
python practica02.py
```

La guía también lista `pynetlogo`, `pandas` y `scipy`; este código solo necesita NumPy y Matplotlib. La visualización en NetLogo (vía pyNetLogo) no está incluida.

## Procedimiento / Metodología

1. **Se analizó la guía:** el sistema de estudio es el crecimiento poblacional y se deben comparar cuatro modelos con el mismo arreglo de datos.
2. **Se estimaron los parámetros a partir de los datos:**
   - P0 = 1000 (primer dato) y 6 períodos (7 datos).
   - r = ln(2100/1000)/6 = **0.1237**, la tasa continua que hace que el modelo exponencial pase por el primer y el último dato.
   - σ = **26.21**, la desviación estándar de las diferencias entre cada dato real y lo que predice el modelo discreto a partir del dato anterior. Es el ruido que realmente tienen los datos.
3. **Modelo determinístico:** P(t) = P0·e^(rt), sin aleatoriedad.
4. **Modelo discreto:** P(t+1) = P(t) + r·P(t), iterado período por período.
5. **Modelo estocástico:** P(t+1) = P(t) + r·P(t) + ε, con ε ~ N(0, σ²), y se corrige a 0 si la población sale negativa. Semilla fija (42) para reproducir resultados.
6. **Modelo continuo:** método de Euler, P(t+Δt) = P(t) + Δt·r·P(t), con Δt = 0.1.
7. **Se compararon los modelos** con el error RMSE contra los datos reales y con la gráfica comparativa.
8. **Se analizaron los efectos** de r, σ y dt con gráficas, y se hizo una simulación Monte Carlo (500 corridas) del modelo estocástico.
9. **Se probó un nuevo arreglo de datos** (decreciente) para ver cómo cambian los parámetros y las curvas.

## Resultados

| t | Dato real | Determinístico | Discreto | Estocástico | Euler (dt=0.1) |
|---|---|---|---|---|---|
| 0 | 1000 | 1000.0 | 1000.0 | 1000.0 | 1000.0 |
| 1 | 1100 | 1131.6 | 1123.7 | 1131.6 | 1130.8 |
| 2 | 1250 | 1280.6 | 1262.6 | 1244.3 | 1278.6 |
| 3 | 1400 | 1449.1 | 1418.7 | 1417.9 | 1445.8 |
| 4 | 1600 | 1639.9 | 1594.2 | 1617.8 | 1634.9 |
| 5 | 1850 | 1855.7 | 1791.3 | 1766.8 | 1848.7 |
| 6 | 2100 | 2100.0 | 2012.8 | 1951.1 | 2090.5 |

| Modelo | RMSE vs. datos |
|---|---|
| Determinístico | 29.21 |
| Discreto | 41.67 |
| Estocástico (una corrida) | 66.31 |
| Continuo (Euler) | 27.20 |

**Interpretación**

- El modelo determinístico y el de Euler son los que mejor siguen los datos. Con r > 0 la población crece exponencialmente, y la curva se vuelve cada vez más empinada, como en los datos.
- El modelo discreto queda por debajo (2012.8 contra 2100) porque usa la misma r en la forma (1 + r)^t, y e^r > 1 + r. Es una diferencia de modelado, no un error de código. Con dt = 1, Euler da exactamente el mismo resultado que el discreto (2012.8).
- Al reducir dt, Euler se acerca a la solución exacta: con dt = 1 el error en t = 6 es 87.2; con 0.5, 45.8; con 0.1, 9.5; con 0.01, 1.0.
- El modelo estocástico es el único que cambia entre corridas. Su RMSE de una sola corrida (66.31) depende de la semilla y no es una medida del modelo. En 500 corridas, la media final es 2009.0, muy cercana al discreto (2012.8), con un rango del 90 % entre 1845.7 y 2156.7. Es decir: en promedio el estocástico sigue al discreto, pero cada trayectoria se desvía.
- Con un nuevo arreglo decreciente (`[500, 480, 450, 430, 390, 370, 340]`) se obtiene r = −0.0643 y σ = 9.31: la población decae exponencialmente, tendiendo a 0 sin hacerse negativa.

## Preguntas de control

**1. ¿Qué representa el arreglo de entrada?**
La serie de observaciones de la población en períodos consecutivos (1000, 1100, …, 2100). De ahí se obtienen P0 (primer valor), el número de períodos, la tasa r y el nivel de ruido σ.

**2. ¿Cuál es la diferencia entre un modelo determinístico y uno estocástico?**
El determinístico no usa aleatoriedad: con los mismos parámetros siempre da el mismo resultado. El estocástico incorpora una variable aleatoria, por lo que cada simulación da una trayectoria distinta y se analiza con muchas corridas (media, percentiles).

**3. ¿Qué efecto produce modificar la tasa (r)?**
Si r > 0, la población crece, y mientras más grande es r, más rápido. Si r = 0, se mantiene constante. Si r < 0, decrece hacia 0. Como el efecto es exponencial, pequeños cambios en r producen grandes diferencias al final (ver `grafica_2_influencia_r.png`).

**4. ¿Qué representa el parámetro σ?**
La desviación estándar del ruido ε ~ N(0, σ²): el nivel de variabilidad o aleatoriedad del sistema. Aquí, σ ≈ 26 personas por período.

**5. ¿Qué ocurre cuando aumenta el nivel de ruido?**
Las trayectorias se dispersan más alrededor del comportamiento promedio, la población final se vuelve menos predecible y aumenta el riesgo de caídas bruscas, incluso hasta 0 (ver `grafica_3_efecto_sigma.png`). Con σ = 0 el modelo estocástico se convierte en el discreto.

**6. ¿Cuál es la diferencia entre los modelos discreto y continuo?**
El discreto cambia en intervalos de tiempo definidos (período a período) y se describe con ecuaciones en diferencias. El continuo supone cambio en todo instante y se describe con la ecuación diferencial dP/dt = rP, que aquí se aproxima con Euler.

**7. ¿Qué función cumple dt?**
Es el tamaño del paso de tiempo en Euler. Un dt grande es más rápido pero menos preciso; un dt pequeño se acerca más a la solución continua exacta, con más cálculo. Con dt = 1, Euler coincide con el modelo discreto.

**8. ¿Por qué es importante visualizar los resultados mediante gráficas?**
Permiten comparar modelos, detectar tendencias (crecimiento o decrecimiento), ver el efecto de los parámetros y la dispersión del ruido, y validar contra los datos reales de forma más clara que una tabla de números.

**9. ¿Qué modelo presenta comportamiento aleatorio?**
El modelo estocástico, por el término ε ~ N(0, σ²). Los otros tres (determinístico, discreto y continuo) siempre producen el mismo resultado.

**10. ¿Cómo cambia la simulación cuando se introduce un nuevo arreglo de datos?**
Cambian los parámetros estimados (P0, r, σ y el número de períodos) y con ellos todas las curvas. Con el arreglo decreciente de prueba, r pasó de 0.1237 a −0.0643 y la población pasó de crecer a decrecer.

## Limitaciones

- Se usó la misma r en los cuatro modelos, como indica la guía; por eso el discreto y el continuo no coinciden exactamente.
- El resultado del estocástico depende de la semilla; por eso se incluyen 500 corridas para el análisis.
- El modelo exponencial no tiene límite de capacidad, por lo que solo es razonable a corto plazo.
