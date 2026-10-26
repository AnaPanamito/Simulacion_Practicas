"""Analisis del efecto de la semilla aleatoria (Python/SimPy) frente a la referencia de Euler.
Ejecutar desde python_sir:  python analisis_aleatoriedad.py
"""
import time
from dataclasses import replace
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sir.dominio.modelo import ConfiguracionSIR
from sir.aplicacion.simulador import SimuladorSIR
from sir.aplicacion.solucion_diferencial import resolver_por_euler

SEMILLAS = range(1, 201)
base = ConfiguracionSIR()

inicio = time.perf_counter()
series = []
for s in SEMILLAS:
    h = SimuladorSIR(replace(base, semilla=s)).ejecutar()
    series.append(np.array([[r.susceptibles, r.infectados, r.recuperados] for r in h]))
duracion = time.perf_counter() - inicio
series = np.array(series)                         # (200, 101, 3)
euler = np.array([[r.susceptibles, r.infectados, r.recuperados] for r in resolver_por_euler(base)])

pico = series[:, :, 1].max(axis=1)
t_pico = series[:, :, 1].argmax(axis=1)
finales_S = series[:, -1, 0]
extinciones = int((series[:, :, 2].max(axis=1) < 30).sum())   # epidemias que casi no prenden

print(f"{len(SEMILLAS)} simulaciones en {duracion:.2f} s ({duracion/len(SEMILLAS)*1000:.1f} ms c/u)")
print(f"Euler       : pico I = {euler[:,1].max():.1f} en t = {euler[:,1].argmax()} | S final = {euler[-1,0]:.1f}")
print(f"SimPy (media): pico I = {pico.mean():.1f} ± {pico.std():.1f} | t pico = {t_pico.mean():.1f} ± {t_pico.std():.1f} | S final = {finales_S.mean():.1f} ± {finales_S.std():.1f}")
print(f"SimPy (rango): pico I [{pico.min():.0f}, {pico.max():.0f}] | t pico [{t_pico.min()}, {t_pico.max()}] | S final [{finales_S.min():.0f}, {finales_S.max():.0f}]")
print(f"Epidemias que casi no prenden (R final < 30): {extinciones} de {len(SEMILLAS)}")
h42 = series[41]
print(f"Semilla 42   : pico I = {h42[:,1].max():.0f} en t = {h42[:,1].argmax()} | S final = {h42[-1,0]:.0f}")

t = np.arange(base.pasos + 1)
fig, ejes = plt.subplots(1, 3, figsize=(15, 4.5), sharex=True)
for k, (nombre, color) in enumerate((("Susceptibles", "tab:blue"), ("Infectados", "tab:red"), ("Recuperados", "tab:green"))):
    for s in range(30):
        ejes[k].plot(t, series[s, :, k], color=color, alpha=.18)
    ejes[k].plot(t, series[:, :, k].mean(axis=0), color=color, lw=2.5, label="Media de 200 semillas")
    ejes[k].plot(t, euler[:, k], "k--", lw=2, label="Euler (determinista)")
    ejes[k].set_title(nombre); ejes[k].set_xlabel("Tiempo (pasos)"); ejes[k].grid(alpha=.3); ejes[k].legend()
ejes[0].set_ylabel("Número de personas")
fig.suptitle("Efecto de la semilla aleatoria: 30 trayectorias (tenues) y media de 200")
plt.tight_layout(); plt.savefig("../results/grafica_semillas.png", dpi=130); plt.close()
