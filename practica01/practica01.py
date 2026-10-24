import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

horas = ["06:00","08:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00"]
hum   = np.array([65,70,68,60,75,85,92,88,80])
nub   = np.array([40,50,45,30,70,85,95,90,75])
temp  = np.array([14,16,18,22,20,18,16,17,15])

def factor_temp(t):
    # <=10 -> 1.0 ; >=28 -> 0.1 ; interpolacion lineal entre 10 y 28 (0.05 por grado)
    return np.clip(1.0 - 0.05 * (t - 10), 0.1, 1.0)

def estado(i):
    if i < 0.40: return "Sin lluvia"
    if i < 0.60: return "Baja posibilidad"
    if i < 0.75: return "Lluvia probable"
    return "Lluvia"

def simular(wh=0.5, wn=0.3, wt=0.2):
    H, N, Tf = hum/100, nub/100, factor_temp(temp)
    return H, N, Tf, wh*H + wn*N + wt*Tf

def tabla(titulo, pesos):
    H, N, Tf, I = simular(*pesos)
    print(f"\n{titulo}  pesos={pesos}")
    print(f"{'Hora':6}{'Hum':>5}{'Nub':>5}{'Temp':>6}{'H':>6}{'N':>6}{'Tf':>6}{'Indice':>8}  Estado")
    for k in range(len(horas)):
        print(f"{horas[k]:6}{hum[k]:5}{nub[k]:5}{temp[k]:6}{H[k]:6.2f}{N[k]:6.2f}{Tf[k]:6.2f}{I[k]:8.3f}  {estado(I[k])}")
    return I

I1 = tabla("MODELO ORIGINAL", (0.5, 0.3, 0.2))
I2 = tabla("MODELO AJUSTADO", (0.4, 0.4, 0.2))

# Grafica 1: indice vs hora con umbrales
for nombre, I in (("original", I1), ("ajustado", I2)):
    plt.figure(figsize=(8,4.5))
    plt.plot(horas, I, "o-", label="Índice I")
    for u, c in ((0.40,"green"),(0.60,"orange"),(0.75,"red")):
        plt.axhline(u, ls="--", color=c, alpha=.6, label=f"umbral {u}")
    plt.title(f"Índice de lluvia por hora (modelo {nombre})")
    plt.xlabel("Hora"); plt.ylabel("I"); plt.ylim(0,1); plt.grid(alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig(f"grafica_indice_{nombre}.png", dpi=130); plt.close()

# Grafica 2: variables normalizadas
H, N, Tf, _ = simular()
plt.figure(figsize=(8,4.5))
plt.plot(horas, H, "o-", label="H"); plt.plot(horas, N, "s-", label="N"); plt.plot(horas, Tf, "^-", label="Tf")
plt.title("Variables normalizadas"); plt.xlabel("Hora"); plt.grid(alpha=.3); plt.legend()
plt.tight_layout(); plt.savefig("grafica_variables.png", dpi=130); plt.close()
