"""Extras Práctica 05: cambio de semilla, Hull-Dobell, períodos con m pequeño y pruebas básicas."""
import math
from lcg import lcg, A, C, M

def periodo(a, c, m, x0):
    visto, x, i = {}, x0, 0
    while x not in visto:
        visto[x] = i
        x = (a * x + c) % m
        i += 1
    return i - visto[x]

print("== Cambio de semilla (10 primeras observaciones) ==")
for s in (1, 987654321, 12345):
    xs, us = lcg(s, 10)
    print("Semilla", s)
    for i in range(10):
        print(f"  {i}  {xs[i]:>12}  {us[i]:.10f}")

print("\n== Hull-Dobell ==")
print("gcd(c,m) =", math.gcd(C, M), "| (a-1) mod 4 =", (A - 1) % 4)

print("\n== Período con m pequeño (mismos a y c) ==")
for k in (10, 16, 20):
    print(f"m=2^{k}: período =", periodo(A, C, 2**k, 12345 % 2**k))

print("\n== Parámetros inadecuados (m=16) ==")
print("a=4,c=2:", periodo(4, 2, 16, 1), "| a=3,c=0:", periodo(3, 0, 16, 1), "| a=5,c=3:", periodo(5, 3, 16, 1))

print("\n== Pruebas básicas (N=10000, semilla 12345) ==")
xs, us = lcg(12345, 10000)
n = len(us); media = sum(us) / n
var = sum((u - media) ** 2 for u in us) / (n - 1)
obs = [0] * 10
for u in us: obs[int(u * 10)] += 1
chi2 = sum((o - n / 10) ** 2 / (n / 10) for o in obs)
mu = media
r1 = sum((us[i] - mu) * (us[i + 1] - mu) for i in range(n - 1)) / sum((u - mu) ** 2 for u in us)
print(f"media={media:.5f} var={var:.5f} chi2={chi2:.3f} (crítico 16.919) autocorr lag1={r1:.4f}")
