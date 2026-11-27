"""
Práctica 08 - Simulación (UNL, Carrera de Computación)
Generación de variables aleatorias mediante el método de la Transformada Inversa.

Ejecutar:  python practica08.py
Salida:    gráficas y tablas en ../resultados/
"""
import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # permite ejecutar sin interfaz gráfica
import matplotlib.pyplot as plt

N = 10_000
SEMILLA = 42
LAMBDA_BASE = 0.5
TASAS = [0.5, 1.0, 2.0]
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")
os.makedirs(SALIDA, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Generación de variables aleatorias uniformes U(0,1)
# ---------------------------------------------------------------------------
def generar_uniformes(n, rng):
    """Genera n números pseudoaleatorios U(0,1), calcula media y varianza
    y construye el histograma."""
    U = rng.random(n)                      # U ~ U(0,1)
    media = U.mean()
    varianza = U.var(ddof=1)               # varianza muestral
    print("=" * 60)
    print("1. GENERACIÓN DE UNIFORMES U(0,1)")
    print("=" * 60)
    print(f"N                    : {n}")
    print(f"Media experimental   : {media:.5f}   (teórica 0.5)")
    print(f"Varianza experimental: {varianza:.5f}   (teórica 1/12 = {1/12:.5f})")

    plt.figure(figsize=(7, 4.5))
    plt.hist(U, bins=20, density=True, edgecolor="black", alpha=0.75,
             label="Muestra U(0,1)")
    plt.axhline(1.0, color="red", linewidth=2, label="Densidad teórica f(u)=1")
    plt.title("Histograma de 10 000 números uniformes U(0,1)")
    plt.xlabel("u")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(SALIDA, "01_histograma_uniforme.png"), dpi=150)
    plt.close()
    return U, media, varianza


# ---------------------------------------------------------------------------
# 2. Transformada Inversa
# ---------------------------------------------------------------------------
def transformada_inversa(U, lam):
    """X = -ln(1 - U) / lambda   (inversa de F(x) = 1 - exp(-lambda x))."""
    if lam <= 0:
        raise ValueError("lambda debe ser mayor que cero")
    return -np.log(1.0 - U) / lam


# ---------------------------------------------------------------------------
# 3. Histograma y comparación con la densidad teórica
# ---------------------------------------------------------------------------
def comparar_distribuciones(X, lam):
    x = np.linspace(0, X.max(), 500)
    f = lam * np.exp(-lam * x)             # densidad teórica

    plt.figure(figsize=(7.5, 4.8))
    plt.hist(X, bins=50, density=True, edgecolor="black", alpha=0.7,
             label="Muestra (Transformada Inversa)")
    plt.plot(x, f, "r-", linewidth=2.2, label=f"f(x) = {lam}·e^(-{lam}x) teórica")
    plt.title(f"Exponencial por Transformada Inversa (λ = {lam}, N = {len(X)})")
    plt.xlabel("x")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(SALIDA, "02_histograma_exponencial_vs_teorica.png"), dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# 4. Comparación de medidas estadísticas
# ---------------------------------------------------------------------------
def comparar_estadisticas(X, lam):
    media_exp = X.mean()
    var_exp = X.var(ddof=1)
    media_teo = 1.0 / lam
    var_teo = 1.0 / lam ** 2
    err_media = abs(media_exp - media_teo) / media_teo * 100
    err_var = abs(var_exp - var_teo) / var_teo * 100
    return {
        "lambda": lam,
        "Media teórica": media_teo,
        "Media experimental": media_exp,
        "Error % media": err_media,
        "Varianza teórica": var_teo,
        "Varianza experimental": var_exp,
        "Error % varianza": err_var,
    }


# ---------------------------------------------------------------------------
# 5. Experimentación con diferentes valores de lambda
# ---------------------------------------------------------------------------
def comparar_valores_lambda(U):
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
    filas = []
    colores = ["tab:blue", "tab:green", "tab:orange"]
    x = np.linspace(0, 8, 500)
    for lam, c in zip(TASAS, colores):
        X = transformada_inversa(U, lam)
        filas.append(comparar_estadisticas(X, lam))
        ax[0].hist(X, bins=80, range=(0, 8), density=True, alpha=0.45,
                   color=c, label=f"λ = {lam}")
        ax[1].plot(x, lam * np.exp(-lam * x), color=c, linewidth=2.2,
                   label=f"λ = {lam}")
    ax[0].set_title("Muestras exponenciales (histogramas)")
    ax[1].set_title("Densidades teóricas")
    for a in ax:
        a.set_xlabel("x")
        a.set_ylabel("Densidad")
        a.legend()
        a.grid(alpha=0.3)
    plt.suptitle("Efecto del parámetro λ en la distribución exponencial")
    plt.tight_layout()
    plt.savefig(os.path.join(SALIDA, "03_comparacion_lambdas.png"), dpi=150)
    plt.close()
    return pd.DataFrame(filas)


def main():
    rng = np.random.default_rng(SEMILLA)

    # 1. Uniformes
    U, media_u, var_u = generar_uniformes(N, rng)

    # 2. Transformada inversa con lambda = 0.5
    print("\n" + "=" * 60)
    print(f"2. TRANSFORMADA INVERSA (λ = {LAMBDA_BASE})")
    print("=" * 60)
    X = transformada_inversa(U, LAMBDA_BASE)
    print("Primeros 10 valores de X:")
    for i, v in enumerate(X[:10], 1):
        print(f"  X[{i:2d}] = {v:.5f}   (U = {U[i-1]:.5f})")
    print(f"Cantidad de datos generados: {len(X)}")
    pd.DataFrame({"U": U, "X_lambda_0.5": X}).to_csv(
        os.path.join(SALIDA, "muestras_lambda_0.5.csv"), index=False)

    # 3. Histograma vs densidad teórica
    comparar_distribuciones(X, LAMBDA_BASE)
    print("\n3. Gráfica de comparación guardada en resultados/")

    # 4 y 5. Estadísticas para cada lambda
    tabla = comparar_valores_lambda(U)
    print("\n" + "=" * 60)
    print("4/5. COMPARACIÓN DE MEDIDAS ESTADÍSTICAS")
    print("=" * 60)
    print(tabla.round(5).to_string(index=False))
    tabla.round(5).to_csv(os.path.join(SALIDA, "tabla_comparativa.csv"), index=False)

    # Resumen de uniformes
    pd.DataFrame([{"N": N, "Media": media_u, "Varianza": var_u,
                   "Media teórica": 0.5, "Varianza teórica": 1 / 12}]
                 ).round(5).to_csv(os.path.join(SALIDA, "resumen_uniformes.csv"), index=False)


if __name__ == "__main__":
    main()
