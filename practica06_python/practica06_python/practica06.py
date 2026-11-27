#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 06 - Simulación (UNL). Validación estadística de números pseudoaleatorios.
Generador LCG + prueba Chi-cuadrado + prueba Kolmogorov-Smirnov + estimación de pi.
Solo usa la biblioteca estándar (math, time, csv, sys). Matplotlib es opcional (gráfico KS).
Uso:  python3 practica06.py
"""
import math, sys, time, csv

ALPHA = 0.05
N_TEST = 10_000          # cantidad de números para las pruebas (Actividad 1, paso 4)
K = 10                   # subintervalos de Chi-cuadrado
# Configuraciones: (nombre, semilla X0, a, c, m)   <-- parámetros propuestos (no los da la guía)
CONFIGS = [
    ("A: Numerical Recipes", 12345, 1664525, 1013904223, 2**32),
    ("B: ANSI C (rand)",     12345, 1103515245, 12345,   2**31),
    ("C: RANDU",             1,     65539,      0,       2**31),
    ("D: periodo corto m=256", 12345, 137,      187,     256),
]

# ---------- Actividad 1: LCG ----------
def lcg(n, seed, a, c, m):
    """Devuelve (estados enteros X1..Xn, valores U_i = X_i/m)."""
    x = seed
    estados, u = [], []
    for _ in range(n):
        x = (a * x + c) % m          # X_{n+1} = (a X_n + c) mod m
        estados.append(x)
        u.append(x / m)              # número en [0,1)
    return estados, u

# ---------- Funciones especiales (sin SciPy, para que Java use exactamente lo mismo) ----------
_LG = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
       -176.61502916214059, 12.507343278686905, -0.13857109526572012,
       9.9843695780195716e-6, 1.5056327351493116e-7]

def lgamma(z):
    """ln Gamma(z) por aproximación de Lanczos (g=7), válida para z >= 0.5."""
    z -= 1.0
    x = _LG[0]
    for i in range(1, 9):
        x += _LG[i] / (z + i)
    t = z + 7.5
    return 0.5 * math.log(2 * math.pi) + (z + 0.5) * math.log(t) - t + math.log(x)

def _gser(a, x):
    gln = lgamma(a); ap = a; s = 1.0 / a; d = s
    for _ in range(1000):
        ap += 1.0; d *= x / ap; s += d
        if abs(d) < abs(s) * 1e-15: break
    return s * math.exp(-x + a * math.log(x) - gln)

def _gcf(a, x):
    tiny = 1e-300
    gln = lgamma(a); b = x + 1.0 - a; c = 1.0 / tiny; d = 1.0 / b; h = d
    for i in range(1, 1000):
        an = -i * (i - a); b += 2.0
        d = an * d + b
        if abs(d) < tiny: d = tiny
        c = b + an / c
        if abs(c) < tiny: c = tiny
        d = 1.0 / d; delta = d * c; h *= delta
        if abs(delta - 1.0) < 1e-15: break
    return math.exp(-x + a * math.log(x) - gln) * h

def chi2_sf(x, gl):
    """P(X >= x) con X ~ chi2(gl) = Q(gl/2, x/2) (gamma incompleta regularizada superior)."""
    if x <= 0: return 1.0
    a, y = gl / 2.0, x / 2.0
    return 1.0 - _gser(a, y) if y < a + 1.0 else _gcf(a, y)

def ks_pvalue(d, n):
    """p-valor asintótico de Kolmogorov con corrección de Stephens: lambda=(sqrt(n)+0.12+0.11/sqrt(n))*D."""
    sn = math.sqrt(n); lam = (sn + 0.12 + 0.11 / sn) * d
    if lam < 0.27: return 1.0
    s = 0.0
    for j in range(1, 101):
        term = 2.0 * (-1) ** (j - 1) * math.exp(-2.0 * j * j * lam * lam)
        s += term
        if abs(term) < 1e-14: break
    return min(1.0, max(0.0, s))

# ---------- Algoritmo 2: Chi-cuadrado ----------
def chi_cuadrado(u, k=K):
    n = len(u); esperada = n / k
    obs = [0] * k
    for v in u:
        obs[int(v * k)] += 1          # intervalo [i/k,(i+1)/k)
    chi2 = 0.0
    for o in obs:
        chi2 += (o - esperada) ** 2 / esperada
    gl = k - 1
    return obs, esperada, chi2, gl, chi2_sf(chi2, gl)

# ---------- Algoritmo 3: Kolmogorov-Smirnov ----------
def kolmogorov_smirnov(u):
    x = sorted(u); n = len(x)
    dpos = dneg = 0.0
    for i, xi in enumerate(x, start=1):
        dpos = max(dpos, i / n - xi)          # D+ = max( i/n - F(x_(i)) )
        dneg = max(dneg, xi - (i - 1) / n)    # D- = max( F(x_(i)) - (i-1)/n )
    d = max(dpos, dneg)
    return x, dpos, dneg, d, ks_pvalue(d, n)

# ---------- Estimación de pi (Monte Carlo con pares consecutivos del LCG) ----------
def estimar_pi(N, seed, a, c, m):
    x = seed; hits = 0
    for _ in range(N):
        x = (a * x + c) % m; u = x / m
        x = (a * x + c) % m; v = x / m
        if u * u + v * v <= 1.0: hits += 1
    return 4.0 * hits / N

def main():
    decision = lambda p: "NO se rechaza H0" if p >= ALPHA else "SE RECHAZA H0"
    for nombre, seed, a, c, m in CONFIGS:
        est, u = lcg(N_TEST, seed, a, c, m)
        print("=" * 70)
        print(f"Configuración {nombre}: X0={seed}, a={a}, c={c}, m={m}, N={N_TEST}")
        print("Primeros 10 números U_i:", " ".join(f"{v:.10f}" for v in u[:10]))
        print(f"Suma de estados enteros = {sum(est)} | último estado = {est[-1]}")
        obs, esp, chi2, gl, p = chi_cuadrado(u)
        print("Chi-cuadrado | Oi =", obs, "| Ei =", f"{esp:.1f}")
        print(f"  chi2 = {chi2:.4f}, gl = {gl}, p = {p:.6f} -> {decision(p)}")
        x, dpos, dneg, d, pk = kolmogorov_smirnov(u)
        print(f"K-S | primeros 3 ordenados = {x[0]:.10f} {x[1]:.10f} {x[2]:.10f}")
        print(f"  D+ = {dpos:.6f}, D- = {dneg:.6f}, D = {d:.6f}, p = {pk:.6f} -> {decision(pk)}")
        # Gráfico ECDF vs CDF (opcional)
        try:
            import matplotlib; matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            n = len(x)
            plt.figure(figsize=(6, 4))
            plt.step(x, [(i + 1) / n for i in range(n)], where="post", label="F_n(x) empírica")
            plt.plot([0, 1], [0, 1], "r--", label="F(x)=x teórica U(0,1)")
            plt.title(f"KS {nombre}\nD={d:.5f}, p={pk:.4f}"); plt.legend(); plt.grid(alpha=.3)
            plt.tight_layout(); plt.savefig(f"ks_{nombre[0]}.png", dpi=120); plt.close()
        except ImportError:
            pass

    # ---- Tabla de resultados esperados (configuración A) ----
    print("=" * 70)
    nombre, seed, a, c, m = CONFIGS[0]
    print(f"Estimación de pi con la configuración {nombre}")
    filas = []
    for N in (1_000, 10_000, 100_000, 1_000_000):
        tiempos = []
        for _ in range(5):
            t0 = time.perf_counter(); pi_est = estimar_pi(N, seed, a, c, m)
            tiempos.append((time.perf_counter() - t0) * 1000)
        tiempos.sort(); t_med = tiempos[2]
        err = abs(pi_est - math.pi)
        print(f"N={N:>9} pi={pi_est:.10f} error={err:.10f}")
        print(f"[Python] N={N} tiempo(mediana de 5)={t_med:.2f} ms", file=sys.stderr)
        filas.append((N, f"{pi_est:.10f}", f"{err:.10f}", f"{t_med:.3f}"))
    with open("tiempos_python.csv", "w", newline="") as f:
        csv.writer(f).writerows([("N", "pi", "error", "ms")] + filas)

if __name__ == "__main__":
    main()
