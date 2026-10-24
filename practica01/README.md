# Práctica 01: Construcción y simulación computacional de un modelo matemático

**Asignatura:** Simulación (Ciclo 5) · **Carrera de Computación, UNL**

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

# Java
javac Practica01.java
java Practica01
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

## Nota

Las preguntas de control de la guía mencionan r, P₀ y el modelo exponencial, que no corresponden a esta práctica. Conviene confirmar con el docente cuáles debes responder.
