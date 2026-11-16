#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparación cruzada Python vs Java (Práctica Nro. 07).
Lee resultados_python.csv y resultados_java.csv, genera:
  - comparacion_final.csv (tabla consolidada)
  - grafico_comparativo.png (error vs N y tiempo vs N)
Uso: python comparar.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RES = os.path.join("..", "resultados")
EVI = os.path.join("..", "evidencias")


def main():
    ruta_py = os.path.join(RES, "resultados_python.csv")
    ruta_jv = os.path.join(RES, "resultados_java.csv")
    for r in (ruta_py, ruta_jv):
        if not os.path.exists(r):
            sys.exit(f"No se encontró {r}. Ejecute primero monte_carlo.py y MonteCarlo.java.")

    py = pd.read_csv(ruta_py)
    jv = pd.read_csv(ruta_jv)

    # Tabla consolidada: une por N
    df = py.merge(jv, on="N", suffixes=("_py", "_java"))
    df = df.rename(columns={
        "pi_estimado_py": "pi_python", "pi_estimado_java": "pi_java",
        "error_absoluto_py": "error_python", "error_absoluto_java": "error_java",
        "tiempo_s_py": "tiempo_python_s", "tiempo_s_java": "tiempo_java_s",
    })[["N", "pi_python", "pi_java", "error_python", "error_java",
        "tiempo_python_s", "tiempo_java_s"]]
    df["diferencia_pi"] = (df["pi_python"] - df["pi_java"]).abs()
    df["razon_tiempo_py_java"] = df["tiempo_python_s"] / df["tiempo_java_s"]
    df.to_csv(os.path.join(RES, "comparacion_final.csv"), index=False)

    # Tabla en consola
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:.6f}")
    print(df.to_string(index=False))

    # Gráficos
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    ax[0].loglog(df["N"], df["error_python"], "o-", label="Python")
    ax[0].loglog(df["N"], df["error_java"], "s--", label="Java")
    ax[0].loglog(df["N"], 1.0 / df["N"] ** 0.5, ":", color="gray", label="Referencia ∝ 1/√N")
    ax[0].set_xlabel("N (puntos)")
    ax[0].set_ylabel("Error absoluto")
    ax[0].set_title("Error absoluto vs N")
    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].legend()

    ax[1].loglog(df["N"], df["tiempo_python_s"], "o-", label="Python")
    ax[1].loglog(df["N"], df["tiempo_java_s"], "s--", label="Java")
    ax[1].set_xlabel("N (puntos)")
    ax[1].set_ylabel("Tiempo (s)")
    ax[1].set_title("Tiempo de ejecución vs N")
    ax[1].grid(True, which="both", alpha=0.3)
    ax[1].legend()

    fig.tight_layout()
    os.makedirs(EVI, exist_ok=True)
    fig.savefig(os.path.join(EVI, "grafico_comparativo.png"), dpi=150)
    print("\nGuardado: comparacion_final.csv y grafico_comparativo.png")


if __name__ == "__main__":
    main()
