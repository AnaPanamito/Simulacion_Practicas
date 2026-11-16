# Práctica Nro. 07 — Estimación de resultados mediante el método de Monte Carlo

**Asignatura:** Simulación · **Ciclo:** 5 · **Carrera de Computación (FEIRNNR) — Universidad Nacional de Loja**

---

## 1. Descripción y objetivos

Se estima el valor de π lanzando puntos aleatorios sobre el cuadrado [-1,1]×[-1,1] y contando cuántos caen dentro del círculo unitario inscrito. El experimento se implementa en **Python** (NumPy, Matplotlib, Pandas) y en **Java** (JDK 17+), con la misma semilla (42), y se comparan estimaciones, errores y tiempos.


## 2. Método y fórmula

- Se generan N puntos (x, y) con x, y ~ U(-1, 1).
- Un punto está **dentro** del círculo si `x² + y² ≤ 1`.
- Área del cuadrado = 4; área del círculo = π. La probabilidad de caer dentro es π/4, que se estima con Nc/N:

```
π ≈ 4 · (Nc / N)         Error absoluto = |π_estimado − π_real|
```

Como Nc ~ Binomial(N, π/4), la desviación estándar de la estimación es σ ≈ 4·√(p(1−p)/N) ≈ **1,64/√N** (p = π/4). Por eso el error típico decrece como 1/√N: para reducir el error 10 veces se necesitan ~100 veces más puntos.

## 3. Estructura del proyecto

```
practica07_montecarlo/
├── README.md
├── python/        monte_carlo.py · comparar.py · requirements.txt
├── java/          MonteCarlo.java · README_java.md
├── resultados/    resultados_python.csv · resultados_java.csv · comparacion_final.csv
│                  resultados_python_replica_java.csv  (extra, ver §7)
└── evidencias/    grafico_puntos.png · grafico_comparativo.png
```

## 4. Requisitos e instalación

- Python 3.9+ y: `pip install numpy matplotlib pandas` (o `pip install -r python/requirements.txt`)
- JDK 17 o superior (`java -version`, `javac -version`)

## 5. Ejecución paso a paso

**Python** (desde la carpeta `python/`):
```bash
cd python
python monte_carlo.py                 # los 4 tamaños; genera resultados_python.csv y grafico_puntos.png
python monte_carlo.py --n 50000       # opcional: un solo N
python monte_carlo.py --seed 42       # semilla configurable (defecto 42)
```

**Java** (desde la carpeta `java/`):
```bash
cd java
javac MonteCarlo.java
java MonteCarlo                       # genera ../resultados/resultados_java.csv
```

**Comparación** (después de ejecutar ambos):
```bash
cd python
python comparar.py                    # genera comparacion_final.csv y grafico_comparativo.png
```

> Los tiempos son la **mediana de 5 ejecuciones**, medidos solo sobre generación + clasificación (sin impresión ni gráficos). Java hace 5 pasadas de calentamiento previas para que el JIT compile el código.

## 6. Resultados obtenidos

Entorno de la corrida incluida: Linux (contenedor), OpenJDK 21, NumPy 2.5.4, Pandas 3.0.6, Matplotlib 3.11.2, semilla 42. **Los tiempos dependen de su equipo; vuelva a ejecutar y reemplace esta tabla con sus propios datos.**

| N | π estimado (Py) | π estimado (Java) | Error Python | Error Java | Tiempo Python (s) | Tiempo Java (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 000 | 3,080000 | 3,312000 | 0,061593 | 0,170407 | 0,000025 | 0,000041 |
| 10 000 | 3,125600 | 3,137200 | 0,015993 | 0,004393 | 0,000109 | 0,000429 |
| 100 000 | 3,143080 | 3,142040 | 0,001487 | 0,000447 | 0,001242 | 0,004380 |
| 1 000 000 | 3,141780 | 3,143472 | 0,000187 | 0,001879 | 0,010744 | 0,047052 |

(π real = 3,1415926536.)

## 7. Sobre la «misma secuencia» exigida por la guía

La guía pide dos implementaciones que *produzcan la misma secuencia con los mismos parámetros*. Con `numpy.random.default_rng(42)` (PCG64) y `java.util.Random(42)` (LCG de 48 bits) **no** ocurre: son algoritmos distintos, así que con igual semilla generan secuencias distintas (tabla anterior). Para cumplir ese requisito, `monte_carlo.py` incluye `--generador java`, que reimplementa el LCG de `java.util.Random` en Python:

```bash
python monte_carlo.py --generador java --repeticiones 3 --salida ../resultados/resultados_python_replica_java.csv
```

Verificado: con ese modo, Python produce **exactamente** los mismos π y errores que Java (3,312 / 3,1372 / 3,14204 / 3,143472). Tiempos con el *mismo algoritmo* (mediana de 3 ejecuciones en Python vs. 5 en Java):

| N | Python (réplica Java) (s) | Java (s) |
|---:|---:|---:|
| 1 000 | 0,000764 | 0,000041 |
| 10 000 | 0,008048 | 0,000429 |
| 100 000 | 0,075499 | 0,004380 |
| 1 000 000 | 0,760181 | 0,047052 |

## 8. Evidencias

- `evidencias/grafico_puntos.png`: N = 10 000, puntos rojos (dentro) y azules (fuera) sobre la circunferencia unitaria; el título muestra π ≈ 3,12560.
- `evidencias/grafico_comparativo.png`: izquierda, error vs N (log-log) con referencia 1/√N; derecha, tiempo vs N (log-log).
- Capturas de consola: ejecute los comandos de la §5 y capture la salida (tabla formateada de cada programa).
- Pendiente según la rúbrica de la guía: **video de demostración** y **defensa oral** (no se generan automáticamente).

## 9. Análisis de resultados (8 preguntas de la guía)

**1. ¿Cómo cambia la estimación de π al aumentar N?**
Tiende a oscilar cada vez más cerca de 3,14159. Con NumPy: 3,080 → 3,126 → 3,143 → 3,1418. No es monótona: es una variable aleatoria cuya dispersión (≈1,64/√N) se reduce al crecer N.

**2. ¿Qué relación existe entre tamaño de muestra y error absoluto?**
El error esperado decrece como 1/√N (convergencia lenta): 100 veces más puntos ≈ 10 veces menos error. En los datos, Python bajó de 0,0616 (N = 10³) a 0,000187 (N = 10⁶), una reducción mayor que la esperada en promedio, por azar de esta semilla. Con una sola muestra por N, el error puntual fluctúa alrededor de esa tendencia.

**3. ¿Con cuál N se obtuvo mejor aproximación?**
Depende del generador. Python/NumPy: **N = 1 000 000** (error 0,000187). Java: **N = 100 000** (error 0,000447; con 10⁶ el error fue 0,001879). Que Java mejore con 10⁵ y no con 10⁶ es un efecto del azar de una única semilla, no del lenguaje.

**4. ¿Qué lenguaje presentó menor tiempo de ejecución?**
En la corrida base, **Python (NumPy vectorizado)** fue ~4 veces más rápido (N = 10⁶: 0,0107 s vs. 0,0471 s), porque NumPy genera y evalúa arreglos completos en código compilado y PCG64 es rápido, mientras que `java.util.Random` es más lento por su diseño (seguro para hilos, con operaciones atómicas por número). Pero la comparación no es «lenguaje contra lenguaje»: al ejecutar el mismo algoritmo en ambos (§7), **Java fue ~16 veces más rápido** que Python con bucle (0,047 s vs. 0,760 s). Conclusión: el resultado depende de la implementación (vectorizada o no) y del generador, además del lenguaje.

**5. ¿Por qué los resultados en Python y Java pueden diferir?**
Porque aunque ambos usen semilla 42, los algoritmos PRNG son distintos (PCG64 vs. LCG de 48 bits), igual que la forma de transformar bits en reales en [0,1). Distinta secuencia ⇒ distinto Nc ⇒ distinto π estimado. Con el mismo generador replicado (§7) los resultados coinciden exactamente. Los tiempos difieren además por JIT, intérprete, vectorización y el estado del sistema.

**6. ¿Qué importancia tiene la generación de números pseudoaleatorios?**
Monte Carlo depende de que las muestras sean uniformes e independientes: un PRNG defectuoso (correlaciones, periodo corto) sesga el resultado. Ser *pseudo*aleatorio permite además **reproducibilidad** (misma semilla ⇒ mismos resultados), clave para depurar, comparar implementaciones y auditar la simulación (principio de transparencia).

**7. ¿Aumentar N garantiza siempre un resultado más cercano al real?**
No. Reduce la dispersión *esperada*, pero cada ejecución sigue siendo aleatoria. Lo muestran los datos de Java: el error con N = 10⁶ (0,001879) es **mayor** que con N = 10⁵ (0,000447). Solo es una garantía probabilística (ley de los grandes números), y el costo crece linealmente con N.

**8. ¿Qué aplicaciones reales tiene Monte Carlo?**
- *Ingeniería:* análisis de confiabilidad y tolerancias, transporte de neutrones/radiación, simulación de colas y redes, análisis de riesgo estructural.
- *Economía y finanzas:* valoración de opciones y derivados, Value at Risk, análisis de riesgo de portafolios, proyecciones con incertidumbre.
- *Informática:* trazado de rayos y renderizado (path tracing), búsqueda en árboles de juegos (MCTS), pruebas de algoritmos aleatorizados, inferencia bayesiana (MCMC).
- *Ciencias:* física estadística y de partículas, dinámica molecular, climatología, epidemiología, integración numérica en altas dimensiones.

## 10. Preguntas de control

**1. ¿Qué es Monte Carlo?**
Una familia de métodos que estiman cantidades numéricas mediante muestreo aleatorio repetido y estadística de los resultados, útil cuando el cálculo analítico es difícil o imposible.

**2. ¿Por qué el error disminuye al aumentar las muestras?**
Por la ley de los grandes números y el teorema del límite central: el promedio de muestras independientes converge a la esperanza y su desviación estándar decrece como σ/√N.

**3. ¿Relación entre precisión y costo computacional?**
Para reducir el error a la mitad hay que cuadruplicar N, y el tiempo crece ~linealmente con N (en los datos, ×10 puntos ≈ ×10 tiempo). La precisión tiene rendimientos decrecientes; se compensa con vectorización, paralelismo o técnicas de reducción de varianza.

**4. ¿Diferencias observadas entre Python y Java?**
(a) Secuencias distintas con la misma semilla por usar PRNG distintos; (b) con NumPy vectorizado Python fue más rápido que Java en esta corrida; (c) con el mismo algoritmo en bucle, Java fue ~16 veces más rápido; (d) Java requiere calentamiento del JIT para medir con justicia.

**5. ¿En qué otros problemas puede usarse Monte Carlo?**
Integrales multidimensionales, valoración de opciones, simulación de colas (M/M/1), análisis de riesgo de proyectos, fiabilidad de sistemas, física de partículas, inferencia bayesiana (MCMC), IA en juegos (MCTS).

## 11. Conclusiones

1. Se implementó el experimento Monte Carlo para estimar π en Python y Java con N = 10³ a 10⁶ y semilla fija.
2. Se comprobó que el error disminuye en promedio ∝ 1/√N, aunque una sola ejecución puede violar la monotonía (Java: 10⁶ peor que 10⁵).
3. La comparación Python/Java depende del generador y de la implementación: NumPy vectorizado fue más rápido; con el mismo algoritmo, Java lo fue. Con el LCG replicado los resultados numéricos son idénticos, lo que cumple el resultado esperado de la guía.
4. La reproducibilidad por semilla permite auditar y contrastar simulaciones, pero un resultado aislado no debe presentarse como «el valor»: para conclusiones sólidas conviene repetir con varias semillas y reportar media e intervalo.


Declaración de uso de inteligencia artificial.

Para el desarrollo de esta práctica utilicé el asistente de IA Claude (Anthropic). La herramienta me proporcionó una propuesta inicial del código en Python y Java, del script de comparación y de la estructura del informe, así como explicaciones teóricas sobre el método de Monte Carlo y los generadores pseudoaleatorios. Yo instalé el entorno, ejecuté ambos programas en mi computador, obtuve y capturé los resultados y evidencias, revisé el código y los resultados, redacté la metodología con mis propias palabras y adapté el análisis a los datos obtenidos. Me hago responsable del contenido entregado y puedo explicar y defender el código y los resultados.
