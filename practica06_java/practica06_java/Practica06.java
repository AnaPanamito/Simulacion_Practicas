import java.io.*;
import java.util.*;

/**
 * Práctica 06 - Simulación (UNL). LCG + Chi-cuadrado + Kolmogorov-Smirnov + estimación de pi.
 * Sin dependencias externas. Ejecutar:  java Practica06.java   (o javac + java Practica06)
 */
public class Practica06 {
    static final double ALPHA = 0.05;
    static final int N_TEST = 10_000, K = 10;

    // {semilla, a, c, m}
    static final String[] NOMBRES = {"A: Numerical Recipes", "B: ANSI C (rand)", "C: RANDU", "D: periodo corto m=256"};
    static final long[][] CFG = {
        {12345L, 1664525L, 1013904223L, 1L << 32},
        {12345L, 1103515245L, 12345L, 1L << 31},
        {1L, 65539L, 0L, 1L << 31},
        {12345L, 137L, 187L, 256L}
    };

    // ---------- LCG ----------
    static long[] estados(int n, long seed, long a, long c, long m) {
        long[] e = new long[n]; long x = seed;
        for (int i = 0; i < n; i++) { x = (a * x + c) % m; e[i] = x; }
        return e;
    }

    // ---------- Funciones especiales ----------
    static final double[] LG = {0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012,
        9.9843695780195716e-6, 1.5056327351493116e-7};

    static double lgamma(double z) {
        z -= 1.0; double x = LG[0];
        for (int i = 1; i < 9; i++) x += LG[i] / (z + i);
        double t = z + 7.5;
        return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }
    static double gser(double a, double x) {
        double gln = lgamma(a), ap = a, s = 1.0 / a, d = s;
        for (int i = 0; i < 1000; i++) {
            ap += 1.0; d *= x / ap; s += d;
            if (Math.abs(d) < Math.abs(s) * 1e-15) break;
        }
        return s * Math.exp(-x + a * Math.log(x) - gln);
    }
    static double gcf(double a, double x) {
        double tiny = 1e-300, gln = lgamma(a), b = x + 1.0 - a, c = 1.0 / tiny, d = 1.0 / b, h = d;
        for (int i = 1; i < 1000; i++) {
            double an = -i * (i - a); b += 2.0;
            d = an * d + b; if (Math.abs(d) < tiny) d = tiny;
            c = b + an / c; if (Math.abs(c) < tiny) c = tiny;
            d = 1.0 / d; double delta = d * c; h *= delta;
            if (Math.abs(delta - 1.0) < 1e-15) break;
        }
        return Math.exp(-x + a * Math.log(x) - gln) * h;
    }
    static double chi2Sf(double x, int gl) {
        if (x <= 0) return 1.0;
        double a = gl / 2.0, y = x / 2.0;
        return y < a + 1.0 ? 1.0 - gser(a, y) : gcf(a, y);
    }
    static double ksPvalue(double d, int n) {
        double sn = Math.sqrt(n), lam = (sn + 0.12 + 0.11 / sn) * d;
        if (lam < 0.27) return 1.0;
        double s = 0.0;
        for (int j = 1; j <= 100; j++) {
            double term = 2.0 * ((j % 2 == 1) ? 1 : -1) * Math.exp(-2.0 * j * j * lam * lam);
            s += term; if (Math.abs(term) < 1e-14) break;
        }
        return Math.min(1.0, Math.max(0.0, s));
    }

    static String decision(double p) { return p >= ALPHA ? "NO se rechaza H0" : "SE RECHAZA H0"; }

    static double estimarPi(int N, long seed, long a, long c, long m) {
        long x = seed; long hits = 0; double md = (double) m;
        for (int i = 0; i < N; i++) {
            x = (a * x + c) % m; double u = x / md;
            x = (a * x + c) % m; double v = x / md;
            if (u * u + v * v <= 1.0) hits++;
        }
        return 4.0 * hits / N;
    }

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out), true, "UTF-8"));
        for (int q = 0; q < CFG.length; q++) {
            long seed = CFG[q][0], a = CFG[q][1], c = CFG[q][2], m = CFG[q][3];
            long[] est = estados(N_TEST, seed, a, c, m);
            double[] u = new double[N_TEST];
            long suma = 0;
            for (int i = 0; i < N_TEST; i++) { u[i] = est[i] / (double) m; suma += est[i]; }
            System.out.println("======================================================================");
            System.out.printf("Configuración %s: X0=%d, a=%d, c=%d, m=%d, N=%d%n", NOMBRES[q], seed, a, c, m, N_TEST);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 10; i++) sb.append(String.format("%.10f", u[i])).append(i < 9 ? " " : "");
            System.out.println("Primeros 10 números U_i: " + sb);
            System.out.println("Suma de estados enteros = " + suma + " | último estado = " + est[N_TEST - 1]);

            // Chi-cuadrado
            int[] obs = new int[K];
            for (double v : u) obs[(int) (v * K)]++;
            double esp = (double) N_TEST / K, chi2 = 0.0;
            for (int o : obs) chi2 += (o - esp) * (o - esp) / esp;
            int gl = K - 1; double p = chi2Sf(chi2, gl);
            System.out.println("Chi-cuadrado | Oi = " + Arrays.toString(obs) + " | Ei = " + String.format("%.1f", esp));
            System.out.printf("  chi2 = %.4f, gl = %d, p = %.6f -> %s%n", chi2, gl, p, decision(p));

            // Kolmogorov-Smirnov
            double[] x = u.clone(); Arrays.sort(x); int n = x.length;
            double dpos = 0.0, dneg = 0.0;
            for (int i = 1; i <= n; i++) {
                dpos = Math.max(dpos, (double) i / n - x[i - 1]);
                dneg = Math.max(dneg, x[i - 1] - (double) (i - 1) / n);
            }
            double d = Math.max(dpos, dneg), pk = ksPvalue(d, n);
            System.out.printf("K-S | primeros 3 ordenados = %.10f %.10f %.10f%n", x[0], x[1], x[2]);
            System.out.printf("  D+ = %.6f, D- = %.6f, D = %.6f, p = %.6f -> %s%n", dpos, dneg, d, pk, decision(pk));
        }

        System.out.println("======================================================================");
        long seed = CFG[0][0], a = CFG[0][1], c = CFG[0][2], m = CFG[0][3];
        System.out.println("Estimación de pi con la configuración " + NOMBRES[0]);
        int[] Ns = {1_000, 10_000, 100_000, 1_000_000};
        try (PrintWriter pw = new PrintWriter("tiempos_java.csv")) {
            pw.println("N,pi,error,ms");
            for (int N : Ns) {
                double[] t = new double[5]; double pi = 0;
                for (int r = 0; r < 5; r++) {
                    long t0 = System.nanoTime(); pi = estimarPi(N, seed, a, c, m);
                    t[r] = (System.nanoTime() - t0) / 1e6;
                }
                Arrays.sort(t); double err = Math.abs(pi - Math.PI);
                System.out.printf("N=%9d pi=%.10f error=%.10f%n", N, pi, err);
                System.err.printf("[Java] N=%d tiempo(mediana de 5)=%.2f ms%n", N, t[2]);
                pw.printf("%d,%.10f,%.10f,%.3f%n", N, pi, err, t[2]);
            }
        }
    }
}
