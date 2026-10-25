"""
Practica 02 - Comparacion de modelos deterministicos, estocasticos, discretos y continuos
Sistema de estudio: crecimiento poblacional.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------- DATOS
datos = np.array([1000, 1100, 1250, 1400, 1600, 1850, 2100], dtype=float)
SEMILLA = 42

# ------------------------------------------------- ESTIMACION DE PARAMETROS
def estimar_parametros(datos):
    """P0, r, sigma y tiempo a partir del arreglo de datos."""
    n = len(datos) - 1                      # numero de periodos
    P0 = datos[0]
    r = np.log(datos[-1] / datos[0]) / n    # tasa continua: P(n) = P0*e^(r*n)
    # ruido observado: diferencia entre el dato real y lo que predice el modelo discreto
    eps = datos[1:] - (datos[:-1] + r * datos[:-1])
    sigma = np.std(eps, ddof=1)
    return P0, r, sigma, n

# ---------------------------------------------------------------- MODELOS
def modelo_deterministico(P0, r, tiempo, puntos=None):
    """P(t) = P0 * e^(r t)"""
    t = np.linspace(0, tiempo, puntos if puntos else tiempo + 1)
    return t, P0 * np.exp(r * t)

def modelo_discreto(P0, r, tiempo):
    """P(t+1) = P(t) + r*P(t)"""
    poblacion = [P0]
    for _ in range(1, tiempo + 1):
        actual = poblacion[-1]
        poblacion.append(actual + r * actual)
    return np.arange(tiempo + 1), np.array(poblacion)

def modelo_estocastico(P0, r, sigma, tiempo, rng):
    """P(t+1) = P(t) + r*P(t) + eps,  eps ~ N(0, sigma^2); no se permite poblacion < 0"""
    poblacion = [P0]
    for _ in range(1, tiempo + 1):
        ruido = rng.normal(0, sigma)
        actual = poblacion[-1]
        nueva = actual + r * actual + ruido
        poblacion.append(max(nueva, 0.0))
    return np.arange(tiempo + 1), np.array(poblacion)

def modelo_continuo_euler(P0, r, tiempo, dt):
    """P(t+dt) = P(t) + dt * (r * P(t))   (aproximacion de dP/dt = rP)"""
    pasos = int(round(tiempo / dt))
    t = np.arange(pasos + 1) * dt
    poblacion = [P0]
    for _ in range(pasos):
        actual = poblacion[-1]
        poblacion.append(actual + dt * (r * actual))
    return t, np.array(poblacion)

def rmse(real, modelo):
    return float(np.sqrt(np.mean((real - modelo) ** 2)))

# ------------------------------------------------------------- EJECUCION
def main():
    rng = np.random.default_rng(SEMILLA)
    P0, r, sigma, tiempo = estimar_parametros(datos)
    dt = 0.1
    t_real = np.arange(tiempo + 1)

    print("=== PARAMETROS ESTIMADOS DEL ARREGLO DE DATOS ===")
    print(f"datos  = {datos.astype(int).tolist()}")
    print(f"P0 = {P0:.0f} | r = {r:.4f} | sigma = {sigma:.2f} | periodos = {tiempo} | dt = {dt}")

    t_det, p_det = modelo_deterministico(P0, r, tiempo)
    t_dis, p_dis = modelo_discreto(P0, r, tiempo)
    t_sto, p_sto = modelo_estocastico(P0, r, sigma, tiempo, rng)
    t_con, p_con = modelo_continuo_euler(P0, r, tiempo, dt)
    p_con_enteros = p_con[::int(round(1 / dt))]       # Euler evaluado en t = 0,1,...,6

    print("\n=== POBLACION POR PERIODO ===")
    print(f"{'t':>3}{'Dato real':>11}{'Determ.':>10}{'Discreto':>10}{'Estoc.':>10}{'Euler':>10}")
    for k in range(tiempo + 1):
        print(f"{k:3d}{datos[k]:11.0f}{p_det[k]:10.1f}{p_dis[k]:10.1f}{p_sto[k]:10.1f}{p_con_enteros[k]:10.1f}")

    print("\n=== ERROR (RMSE) CONTRA LOS DATOS REALES ===")
    for nombre, serie in (("Deterministico", p_det), ("Discreto", p_dis),
                          ("Estocastico", p_sto), ("Continuo (Euler)", p_con_enteros)):
        print(f"{nombre:18s}: {rmse(datos, serie):8.2f}")

    # ---------- Grafica 1: comparacion de los cuatro modelos
    plt.figure(figsize=(9, 5))
    plt.plot(t_real, datos, "ko", label="Datos reales")
    plt.plot(np.linspace(0, tiempo, 200), P0*np.exp(r*np.linspace(0, tiempo, 200)), "b-", label="Determinístico  P0·e^(rt)")
    plt.plot(t_dis, p_dis, "gs--", label="Discreto  P+rP")
    plt.plot(t_sto, p_sto, "r^-", label=f"Estocástico (σ={sigma:.1f})")
    plt.plot(t_con, p_con, "m-", alpha=.7, label=f"Continuo Euler (dt={dt})")
    plt.title("Comparación de los cuatro modelos de crecimiento poblacional")
    plt.xlabel("Tiempo"); plt.ylabel("Población"); plt.grid(alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig("grafica_1_comparacion_modelos.png", dpi=130); plt.close()

    # ---------- Grafica 2: influencia de r (crecimiento y decrecimiento)
    plt.figure(figsize=(9, 5))
    for rv in (-0.10, -0.05, 0.0, 0.05, r, 0.20):
        t, p = modelo_deterministico(P0, rv, tiempo, 200)
        et = "decrecimiento" if rv < 0 else ("constante" if rv == 0 else "crecimiento")
        plt.plot(t, p, label=f"r = {rv:.3f} ({et})")
    plt.title("Influencia de la tasa r (modelo determinístico)")
    plt.xlabel("Tiempo"); plt.ylabel("Población"); plt.grid(alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig("grafica_2_influencia_r.png", dpi=130); plt.close()

    # ---------- Grafica 3: efecto de sigma (10 corridas por nivel)
    niveles = (0, sigma, 3*sigma, 6*sigma)
    fig, ejes = plt.subplots(2, 2, figsize=(11, 7), sharex=True, sharey=True)
    for ax, s in zip(ejes.ravel(), niveles):
        for _ in range(10):
            t, p = modelo_estocastico(P0, r, s, tiempo, rng)
            ax.plot(t, p, alpha=.6)
        ax.plot(t_dis, p_dis, "k--", lw=2, label="Discreto (sin ruido)")
        ax.set_title(f"σ = {s:.1f}"); ax.grid(alpha=.3); ax.legend()
    fig.supxlabel("Tiempo"); fig.supylabel("Población")
    fig.suptitle("Efecto del nivel de ruido σ (10 simulaciones por nivel)")
    plt.tight_layout(); plt.savefig("grafica_3_efecto_sigma.png", dpi=130); plt.close()

    # ---------- Grafica 4: Monte Carlo del modelo estocastico
    corridas = np.array([modelo_estocastico(P0, r, sigma, tiempo, rng)[1] for _ in range(500)])
    media = corridas.mean(axis=0)
    p5, p95 = np.percentile(corridas, [5, 95], axis=0)
    plt.figure(figsize=(9, 5))
    plt.fill_between(t_real, p5, p95, alpha=.25, color="red", label="Banda 5%-95% (500 corridas)")
    plt.plot(t_real, media, "r-", label="Media estocástica")
    plt.plot(t_dis, p_dis, "g--", label="Discreto (determinístico)")
    plt.plot(t_real, datos, "ko", label="Datos reales")
    plt.title("Modelo estocástico: 500 simulaciones"); plt.xlabel("Tiempo"); plt.ylabel("Población")
    plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
    plt.savefig("grafica_4_montecarlo.png", dpi=130); plt.close()
    print(f"\nMonte Carlo (500 corridas): media final = {media[-1]:.1f}, "
          f"percentiles 5-95 = [{p5[-1]:.1f}, {p95[-1]:.1f}], discreto final = {p_dis[-1]:.1f}")

    # ---------- Grafica 5: efecto de dt en el modelo continuo
    plt.figure(figsize=(9, 5))
    t_ex, p_ex = modelo_deterministico(P0, r, tiempo, 300)
    plt.plot(t_ex, p_ex, "k-", lw=2, label="Solución exacta P0·e^(rt)")
    print("\n=== EFECTO DE dt (poblacion final en t=6, exacta = %.1f) ===" % p_ex[-1])
    for d in (1.0, 0.5, 0.1, 0.01):
        t, p = modelo_continuo_euler(P0, r, tiempo, d)
        plt.plot(t, p, label=f"Euler dt={d}")
        print(f"dt = {d:5}: P(6) = {p[-1]:8.1f} | error = {abs(p[-1]-p_ex[-1]):6.1f}")
    plt.title("Efecto del paso dt en el modelo continuo (Euler)")
    plt.xlabel("Tiempo"); plt.ylabel("Población"); plt.grid(alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig("grafica_5_efecto_dt.png", dpi=130); plt.close()

    # ---------- Nuevo arreglo de datos (pregunta 10)
    nuevo = np.array([500, 480, 450, 430, 390, 370, 340], dtype=float)
    P0n, rn, sn, tn = estimar_parametros(nuevo)
    print(f"\n=== NUEVO ARREGLO {nuevo.astype(int).tolist()} ===")
    print(f"P0 = {P0n:.0f} | r = {rn:.4f} (negativo = decrecimiento) | sigma = {sn:.2f}")
    plt.figure(figsize=(9, 5))
    plt.plot(np.arange(tn+1), nuevo, "ko", label="Datos reales")
    t, p = modelo_deterministico(P0n, rn, tn, 200); plt.plot(t, p, "b-", label="Determinístico")
    t, p = modelo_discreto(P0n, rn, tn); plt.plot(t, p, "gs--", label="Discreto")
    t, p = modelo_estocastico(P0n, rn, sn, tn, rng); plt.plot(t, p, "r^-", label="Estocástico")
    t, p = modelo_continuo_euler(P0n, rn, tn, dt); plt.plot(t, p, "m-", alpha=.7, label="Euler")
    plt.title("Nuevo arreglo de datos (decrecimiento, r < 0)")
    plt.xlabel("Tiempo"); plt.ylabel("Población"); plt.grid(alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig("grafica_6_nuevo_arreglo.png", dpi=130); plt.close()

if __name__ == "__main__":
    main()
