# Práctica 01: Construcción y simulación computacional de un modelo matemático

**Asignatura:** Simulación (Ciclo 5) · **Carrera de Computación, UNL**
**Estudiante:** Ana Panamito 

Simulación del comportamiento de la atmósfera durante 24 horas para determinar en qué horas el modelo considera que existe posibilidad de lluvia.

## Archivos

| Archivo | Descripción |
|---|---|
| `practica01.py` | Implementación en Python (NumPy + Matplotlib). Imprime las tablas y genera las gráficas. |
| `Practica01.java` | Implementación equivalente en Java. Imprime las tablas en consola. |
| `grafica_indice_original.png` | Índice I por hora con el modelo original. |
| `grafica_indice_ajustado.png` | Índice I por hora con el modelo ajustado. |
| `grafica_variables.png` | H, N y Tf normalizadas por hora. |

## Cómo ejecutar

```bash
# Python (requiere numpy y matplotlib)
pip install numpy matplotlib
python3 practica01.py

```

## Conceptos clave

**Modelo matemático.** Representación simplificada de un fenómeno real mediante variables y relaciones matemáticas. Aquí el fenómeno es la posibilidad de lluvia y la relación es una fórmula que combina humedad, nubosidad y temperatura.

**Variables.** Cantidades que cambian en el tiempo y se miden u observan. En la práctica: humedad (%), nubosidad (%) y temperatura (°C) en cada hora.

**Parámetros.** Valores fijos que definen el comportamiento del modelo y que podemos ajustar. Aquí son los pesos de la fórmula (0.5, 0.3, 0.2) y los umbrales de la tabla de reglas (0.40, 0.60, 0.75).

**Normalización.** Convertir cada variable a una escala común de 0 a 1 para poder combinarlas. Humedad y nubosidad se dividen entre 100 (90 % → H = 0.9).

**Factor de temperatura (Tf).** Transforma la temperatura en un valor entre 0.1 y 1.0: a menor temperatura, mayor Tf, porque el aire frío favorece la lluvia en este modelo. Para temperaturas que no están en la tabla (15 °C, 17 °C) se interpoló linealmente: `Tf = 1 − 0.05·(T − 10)`, limitado entre 0.1 y 1.0.

**Índice de lluvia (I).** Combinación lineal ponderada de las tres variables:

```
I = 0.5·H + 0.3·N + 0.2·Tf
```

Como los pesos suman 1 y cada variable está entre 0 y 1, I también queda entre 0 y 1.

**Tabla de reglas (clasificación).** Convierte el valor numérico de I en un estado:

| Índice I | Estado |
|---|---|
| I < 0.40 | Sin lluvia |
| 0.40 ≤ I < 0.60 | Baja posibilidad |
| 0.60 ≤ I < 0.75 | Lluvia probable |
| I ≥ 0.75 | Lluvia |

**Simulación.** Evaluar el modelo repetidamente con distintos datos de entrada (aquí, 9 horas del día) para observar cómo se comporta el sistema.

**Ajuste del modelo.** Modificar los parámetros para mejorar o cambiar el resultado. Se probaron los pesos 0.4H + 0.4N + 0.2Tf (más importancia a la nubosidad). Solo cambió el estado de las 06:00, de *Lluvia probable* a *Baja posibilidad*.

**Análisis gráfico.** Las gráficas muestran la evolución del índice durante el día junto con los umbrales, lo que permite ver cuándo el sistema cruza de un estado a otro. En los datos, el índice es bajo al mediodía (12:00) y crece hasta alcanzar su máximo a las 18:00, cuando humedad y nubosidad son más altas.

## Resultados en una línea

Con ambos modelos, la lluvia se predice desde las 16:00 hasta las 22:00, con el pico a las 18:00 (I ≈ 0.89).

## Preguntas de control 
**a.	¿Qué es un modelo matemático?**
Es un modelo simplificado de un fenómeno o sistema del mundo real, construido usando variables, parámetros y relaciones matemáticas (como ecuaciones, fórmulas y reglas) para describir, simular y predecir el comportamiento del sistema. En este ejercicio, el modelo se define como I = 0,5H + 0,3N + 0,2Tf, que se utiliza para predecir la probabilidad de lluvia.
**b.	¿Cuál es la diferencia entre variable y parámetro?**
Variable: Valor que cambia durante una simulación o en función de condiciones específicas. Ejemplo: humedad, turbidez y temperatura por hora.
Parámetro: Valor fijo que determina el comportamiento del modelo y puede ser ajustado entre simulaciones. Ejemplo: pesos de 0,5, 0,3 y 0,2, con umbrales de 0.40, 0.60 y 0.75.
**c.	¿Qué representa P₀?**
En el modelo exponencial P(t) = P₀·e^(rt), P₀ representa el valor inicial de la cantidad en análisis (población, dinero, etc.) en el tiempo t = 0. Este es el punto de referencia desde el cual el modelo comienza a crecer o decrecer.
**d.	¿Qué ocurre cuando r < 0?**
La función tiene decrecimiento exponencial: P disminuye con el tiempo y tiende a cero sin llegar a ser negativa.Es el comportamiento de fenómenos como la desintegración radiactiva o la depreciación. Si r > 0 hay crecimiento, y si r = 0 el valor se mantiene constante en P₀
**e.	¿Qué limitaciones tiene el modelo exponencial?**
Supone que la tasa r es constante, algo poco realista a largo plazo. Con r > 0 crece sin límite, pero en la realidad hay restricciones. No considera factores externos, como competencia, enfermedades o cambios del entorno. Solo describe bien el comportamiento en un rango corto de tiempo. Por eso, para casos más realistas se usan modelos como el logístico, que incorpora un límite de capacidad.

## Declaración de IA 
Para el desarrollo de esta práctica utilicé Claude (Anthropic) como herramienta de apoyo. La IA colaboró en la explicación de conceptos de modelación matemática, en la generación de una propuesta de código en Python y Java, en la elaboración de las tablas y gráficas, y en la redacción de borradores del README y del procedimiento. Posteriormente revisé el código, lo ejecuté y verifiqué los resultados, comprendí la lógica del modelo (normalización, factor de temperatura, índice y reglas de clasificación) y asumo la responsabilidad del contenido presentado, en concordancia con los principios de transparencia, responsabilidad y honestidad de la asignatura.

