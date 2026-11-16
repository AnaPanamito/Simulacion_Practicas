#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica Nro. 07 - Simulación (UNL, Carrera de Computación)
Estimación de π mediante el método de Monte Carlo (implementación en Python).

Uso:
    python monte_carlo.py                      # recorre N = 1e3, 1e4, 1e5, 1e6
    python monte_carlo.py --n 50000            # un único tamaño de muestra
    python monte_carlo.py --seed 7             # otra semilla
    python monte_carlo.py --generador java     # réplica exacta de java.util.Random

Generadores disponibles:
    numpy (por defecto): np.random.default_rng(seed) -> PCG64, vectorizado.
    java               : port de java.util.Random (LCG de 48 bits). Produce la
                         MISMA secuencia que MonteCarlo.java (semilla 42), pero
                         necesita un bucle explícito (el LCG es secuencial).
"""
import argparse
import math
import os
import statistics
import time

import matplotlib
matplotlib.use("Agg")  # backend sin ventana: guarda la figura directamente
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TAMANOS = [1_000, 10_000, 100_000, 1_000_000]
SEMILLA_POR_DEFECTO = 42
N_GRAFICO = 10_000          # tamaño usado para la evidencia visual
PI_REAL = math.pi


# --------------------------------------------------------------------------
# Generador compatible con java.util.Random (opcional, para réplica exacta)
# --------------------------------------------------------------------------
class JavaRandom:
    """Port de java.util.Random: LCG de 48 bits (multiplicador 0x5DEECE66D)."""
    _MULT = 0x5DEECE66D
    _MASK = (1 << 48) - 1

    def __init__(self, semilla: int):
        self.s = (semilla ^ self._MULT) & self._MASK

    def _next(self, bits: int) -> int:
        self.s = (self.s * self._MULT + 0xB) & self._MASK
        return self.s >> (48 - bits)

    def next_double(self) -> float:
        # Igual que Random.nextDouble(): ((next(26) << 27) + next(27)) * 2^-53
        return ((self._next(26) << 27) + self._next(27)) * (1.0 / (1 << 53))


# --------------------------------------------------------------------------
# Núcleo del experimento: generación + clasificación (lo ÚNICO que se cronometra)
# --------------------------------------------------------------------------
def generar_y_clasificar_numpy(n: int, semilla: int):
    """Versión vectorizada con NumPy (sin bucles for explícitos)."""
    rng = np.random.default_rng(semilla)
    x = rng.uniform(-1.0, 1.0, n)           # coordenadas en [-1, 1)
    y = rng.uniform(-1.0, 1.0, n)
    dentro = (x * x + y * y) <= 1.0          # máscara booleana: x²+y² ≤ 1
    return x, y, dentro


def generar_y_clasificar_java(n: int, semilla: int):
    """Versión con bucle que replica java.util.Random (misma secuencia que Java)."""
    r = JavaRandom(semilla)
    x = np.empty(n)
    y = np.empty(n)
    for i in range(n):
        x[i] = 2.0 * r.next_double() - 1.0   # x primero, luego y (igual que en Java)
        y[i] = 2.0 * r.next_double() - 1.0
    dentro = (x * x + y * y) <= 1.0
    return x, y, dentro


def obtener_funcion(generador: str):
    return generar_y_clasificar_java if generador == "java" else generar_y_clasificar_numpy


def ejecutar_experimento(n: int, semilla: int, generador: str, repeticiones: int):
    """Ejecuta el experimento para un N y devuelve (pi_est, error, tiempo_s).

    El tiempo es la MEDIANA de `repeticiones` ejecuciones (reduce el ruido del
    sistema). La estimación de π es idéntica en todas porque la semilla es fija.
    """
    funcion = obtener_funcion(generador)
    tiempos = []
    nc = 0
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        _, _, dentro = funcion(n, semilla)
        nc = int(np.count_nonzero(dentro))   # Nc: puntos dentro del círculo
        t1 = time.perf_counter()
        tiempos.append(t1 - t0)
    pi_est = 4.0 * nc / n                     # π ≈ 4 · (Nc / N)
    error = abs(pi_est - PI_REAL)             # error absoluto
    return pi_est, error, statistics.median(tiempos)


# --------------------------------------------------------------------------
# Evidencia visual
# --------------------------------------------------------------------------
def graficar_puntos(n: int, semilla: int, generador: str, ruta: str):
    x, y, dentro = obtener_funcion(generador)(n, semilla)
    pi_est = 4.0 * np.count_nonzero(dentro) / n
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(x[dentro], y[dentro], s=2, c="red", label="Dentro del círculo")
    ax.scatter(x[~dentro], y[~dentro], s=2, c="blue", label="Fuera del círculo")
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(t), np.sin(t), "k-", lw=1)  # circunferencia unitaria
    ax.set_aspect("equal")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_title(f"Monte Carlo: N = {n:,}  |  π ≈ {pi_est:.5f}  (semilla {semilla})")
    ax.legend(loc="upper right", markerscale=5)
    fig.tight_layout()
    os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# Programa principal
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Estimación de π por Monte Carlo (Python)")
    ap.add_argument("--n", type=int, default=None,
                    help="Tamaño de muestra único (si se omite, recorre los 4 tamaños)")
    ap.add_argument("--seed", type=int, default=SEMILLA_POR_DEFECTO, help="Semilla (defecto 42)")
    ap.add_argument("--generador", choices=["numpy", "java"], default="numpy",
                    help="numpy (vectorizado) o java (réplica de java.util.Random)")
    ap.add_argument("--repeticiones", type=int, default=5,
                    help="Repeticiones para la mediana del tiempo (defecto 5)")
    ap.add_argument("--salida", default=os.path.join("..", "resultados", "resultados_python.csv"))
    ap.add_argument("--grafico", default=os.path.join("..", "evidencias", "grafico_puntos.png"))
    args = ap.parse_args()

    tamanos = [args.n] if args.n else TAMANOS

    # Calentamiento (no se registra): evita medir la carga inicial de NumPy.
    obtener_funcion(args.generador)(1_000, args.seed)

    filas = []
    for n in tamanos:
        pi_est, err, t = ejecutar_experimento(n, args.seed, args.generador, args.repeticiones)
        filas.append({"N": n, "pi_estimado": pi_est, "error_absoluto": err, "tiempo_s": round(t, 6)})

    df = pd.DataFrame(filas)
    os.makedirs(os.path.dirname(args.salida) or ".", exist_ok=True)
    df.to_csv(args.salida, index=False)

    # Resumen en consola
    print("=" * 68)
    print(f" Monte Carlo (Python) | generador={args.generador} | semilla={args.seed}")
    print(f" π real = {PI_REAL:.10f} | tiempo = mediana de {args.repeticiones} ejecuciones")
    print("=" * 68)
    print(f"{'N':>12} | {'π estimado':>12} | {'Error abs.':>12} | {'Tiempo (s)':>11}")
    print("-" * 68)
    for f in filas:
        print(f"{f['N']:>12,} | {f['pi_estimado']:>12.6f} | {f['error_absoluto']:>12.6f} | {f['tiempo_s']:>11.6f}")
    print("-" * 68)
    print(f"CSV guardado en: {args.salida}")

    # Gráfico de puntos para N = 10 000 (fuera de la medición de tiempos)
    graficar_puntos(N_GRAFICO, args.seed, args.generador, args.grafico)
    print(f"Gráfico guardado en: {args.grafico}")


if __name__ == "__main__":
    main()
