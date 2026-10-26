# Practica 004 - SIR modular (corregido segun la guia)

**Objetivo:** comparar el modelo SIR implementado en Python/SimPy y NetLogo (el docente indico que solo se hacen estas dos herramientas). Se conserva la arquitectura por capas, con identificadores propios en espanol.

## Python
Desde `python_sir`:
```bash
python -m pip install -r requirements.txt
python -m sir.presentacion.consola
```
Usa `--csv`, `--grafica`, `--semilla` para cambiar salidas/semilla. Genera el CSV de SimPy, el grafico y un CSV Euler adicional.

## NetLogo
Abra `netlogo/modelo_sir_netlogo.nlogo` con NetLogo 6.x/7.x (ya incluye botones, monitores y 5 graficas). El archivo debe estar en la misma carpeta que `resultados_python.csv`.
1. Pulse **Ejecutar todo (automatico)**: prepara, corre los 100 pasos, carga el CSV de Python y guarda `resultados_netlogo.csv`.
2. Alternativa manual: **Preparar** -> **Avanzar (forever)** -> **Cargar Python (CSV)**.
Si el `.nlogo` no abre, cree un modelo nuevo, pegue `modelo_sir_netlogo.nls` en la pestana Code y cree los plots con los nombres exactos: `SIR NetLogo` y `SIR Python` (pens `S`, `I`, `R`); `Comparacion infectados`, `Comparacion susceptibles` y `Comparacion recuperados` (pens `Python`, `NetLogo`).

## Analisis de aleatoriedad (Python)
`python analisis_aleatoriedad.py` (desde `python_sir`) corre 200 semillas y genera `results/grafica_semillas.png`.


## ventajas y limitaciones de cada herramienta
**NetLogo**
Ventajas: permite ver inmediatamente a los agentes, tiene una interfaz gráfica sin necesidad de programar y es fácil de explicar a otros.
Limitaciones: es lento al hacer muchas corridas, tiene pocas herramientas de análisis estadístico y depende de su propio entorno.

**Python/SimPy**
Ventajas: es rápido, fácil de automatizar y repetir, permite analizar resultados (con 200 semillas, comparación con Euler) y probarlos con tests.
Limitaciones: la visualización es estática y no muestra movimiento de los agentes sin librerías adicionales.

## Verificaciones
- 101 filas por ejecucion, pasos 0..100.
- Primer registro: `0,95,5,0`.
- Conservacion `S+I+R=100` para todas las filas.
- Ningun infectado recuperado regresa a ser susceptible.
- Puede haber diferencias entre Python y NetLogo por los PRNG.

## Preguntas de control 
**1. ¿Qué representa el modelo SIR?**
Muestra cómo se extiende una enfermedad en una población con tres grupos: susceptibles, infectados y recuperados.

**2. ¿Qué representan los estados S, I y R?**
S son las personas que pueden contraer la enfermedad, I son las que la tienen y la transmiten, y R son las que ya se han recuperado. Siempre se cumple que S + I + R = N.

**3. ¿Qué función cumplen los parámetros β y γ?**
β es la velocidad con que se contagia (0,30), y γ es la tasa de recuperación (0,10). La división entre ellas da R₀ = 3.

**4. ¿Por qué es importante utilizar los mismos parámetros en las tres herramientas?**
Para que los resultados difieran solo por la herramienta o el azar, no por el modelo. Así se garantiza una comparación justa.

**5. ¿Por qué Python, Java y NetLogo pueden producir resultados diferentes utilizando el mismo modelo?**
Porque el modelo incluye elementos aleatorios y cada herramienta maneja esos números de forma diferente.

**6. ¿Qué ventajas ofrece NetLogo para representar sistemas basados en agentes?**
Cada persona es un agente con su estado propio, se puede ver su cambio en tiempo real y tiene gráficas y controles integrados.

**7. ¿Qué ventajas ofrece SimPy para desarrollar simulaciones basadas en eventos?**
Automatiza la gestión del tiempo y los procesos, sin necesidad de programar un reloj manual. Además es código Python, facilitando el análisis y las gráficas.

**8. ¿Qué	ventajas	ofrece	Java	para	implementar modelos de simulación?**
Es rápido, tiene tipado fuerte, es orientado a objetos y se puede usar en grandes proyectos. Su desventaja es que requiere más código.

**9. ¿Qué función cumple el archivo CSV en la integración Python/Java → NetLogo?**
Es un archivo con datos de tiempo, susceptibles, infectados y recuperados. Python lo crea y NetLogo lo usa para graficar, sin tener que recalcular.

**10. ¿Qué ventajas presenta separar la generación de datos de la visualización?**
Cada herramienta se encarga de lo que hace mejor: Python calcula, NetLogo muestra. Se pueden repetir gráficos sin volver a simular y los datos se pueden usar en otras herramientas o revisar.

## Declaración de IA 
Para esta práctica utilicé Claude (Anthropic) como herramienta de apoyo. La IA revisó y verificó el proyecto de Python ya existente, propuso el modelo de NetLogo con su interfaz, un script de análisis de aleatoriedad (200 semillas) y la línea de movimiento visual, ajustó los tests y el README, y ayudó a corregir y aclarar conceptos (modelo SIR, R₀, diferencias por números aleatorios) y a redactar borradores del informe. Ejecuté los programas en mi equipo, comprobé los resultados, realicé la simulación en NetLogo, tomé las capturas, y revisé y adapté los textos con mis propias observaciones. Asumo la responsabilidad del contenido presentado, en concordancia con los principios de transparencia, responsabilidad y honestidad de la asignatura




