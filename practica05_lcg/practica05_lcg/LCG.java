import java.io.*;

/** Práctica 05 - LCG en Java. X(n+1) = (a*X(n)+c) mod 2^32 ; U(n) = X(n)/m */
public class LCG {
    static final long A = 1664525L, C = 1013904223L, M = 1L << 32;
    static final long MASK = 0xFFFFFFFFL;      // x mod 2^32 == x & 0xFFFFFFFF

    static long siguiente(long x) {
        // x < 2^32 y A < 2^21  => A*x < 2^53: cabe en long (64 bits); se enmascara.
        return (A * x + C) & MASK;
    }

    static void generar(long semilla, int n, String archivo) throws IOException {
        try (PrintWriter pw = new PrintWriter(new FileWriter(archivo))) {
            pw.println("n,Xn,Un");
            long x = semilla;
            for (int i = 0; i < n; i++) {
                double u = (double) x / M;
                pw.printf(java.util.Locale.US, "%d,%d,%.10f%n", i, x, u);
                if (i < 20 && archivo.equals("lcg_java.csv"))
                    System.out.printf(java.util.Locale.US, "%3d %12d %.10f%n", i, x, u);
                x = siguiente(x);
            }
        }
    }

    public static void main(String[] args) throws IOException {
        System.out.println("  n          X_n          U_n");
        generar(12345L, 10_000, "lcg_java.csv");
        // período: se avanza hasta volver a la semilla (≈ 4.29e9 iteraciones)
        long x = siguiente(12345L), pasos = 1;
        while (x != 12345L) { x = siguiente(x); pasos++; }
        System.out.println("Periodo observado (semilla 12345) = " + pasos);
        for (long s : new long[]{1L, 987654321L}) {
            x = siguiente(s); pasos = 1;
            while (x != s) { x = siguiente(x); pasos++; }
            System.out.println("Periodo observado (semilla " + s + ") = " + pasos);
        }
    }
}
