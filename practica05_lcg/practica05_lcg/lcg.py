"""Práctica 05 - LCG en Python. X(n+1) = (a*X(n)+c) mod m ; U(n)=X(n)/m"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A, C, M = 1664525, 1013904223, 2**32   # Numerical Recipes
SEMILLA, N = 12345, 10_000

def lcg(semilla, n, a=A, c=C, m=M):
    """Devuelve listas (X, U) con X_0..X_{n-1}; X_0 es la semilla."""
    xs, us = [], []
    x = semilla
    for _ in range(n):
        xs.append(x)
        us.append(x / m)
        x = (a * x + c) % m
    return xs, us

def guardar_csv(nombre, xs, us):
    with open(nombre, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "Xn", "Un"])
        for i, (x, u) in enumerate(zip(xs, us)):
            w.writerow([i, x, f"{u:.10f}"])

if __name__ == "__main__":
    xs, us = lcg(SEMILLA, N)
    print(f"{'n':>3} {'X_n':>12} {'U_n':>12}")
    for i in range(20):
        print(f"{i:>3} {xs[i]:>12} {us[i]:>12.10f}")
    guardar_csv("lcg_python.csv", xs, us)

    fig, ax = plt.subplots(1, 3, figsize=(17, 4.5))
    ax[0].plot(range(N), us, ".", ms=1.5); ax[0].set_title("U_n vs n (10 000 valores)")
    ax[0].set_xlabel("n"); ax[0].set_ylabel("U_n")
    ax[1].hist(us, bins=20, edgecolor="k"); ax[1].set_title("Histograma de U_n")
    ax[2].plot(us[:-1], us[1:], ".", ms=1.5); ax[2].set_title("Diagrama (U_n, U_{n+1})")
    ax[2].set_xlabel("U_n"); ax[2].set_ylabel("U_{n+1}")
    plt.tight_layout(); plt.savefig("lcg_grafica.png", dpi=130)
    print("media =", sum(us)/N, " varianza =", sum((u-sum(us)/N)**2 for u in us)/(N-1))
