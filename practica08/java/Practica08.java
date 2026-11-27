import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Locale;
import java.util.Random;

/**
 * Práctica 08 - Simulación (UNL, Carrera de Computación)
 * Generación de variables aleatorias por el método de la Transformada Inversa.
 *
 * Compilar: javac Practica08.java
 * Ejecutar: java Practica08
 * Genera:   ../resultados/java_tabla_comparativa.csv y java_histograma_lambda_0.5.csv
 */
public class Practica08 {

    static final int N = 10_000;
    static final long SEMILLA = 42L;
    static final double LAMBDA_BASE = 0.5;
    static final double[] TASAS = {0.5, 1.0, 2.0};

    // ---------- Utilidades estadísticas ----------
    static double media(double[] v) {
        double s = 0;
        for (double d : v) s += d;
        return s / v.length;
    }

    static double varianza(double[] v) {          // varianza muestral (n-1)
        double m = media(v), s = 0;
        for (double d : v) s += (d - m) * (d - m);
        return s / (v.length - 1);
    }

    // ---------- 1. Uniformes ----------
    static double[] generarUniformes(int n, Random rnd) {
        double[] u = new double[n];
        for (int i = 0; i < n; i++) u[i] = rnd.nextDouble();   // U ~ U(0,1)
        System.out.println("=== 1. UNIFORMES U(0,1) ===");
        System.out.printf(Locale.US, "N = %d%n", n);
        System.out.printf(Locale.US, "Media experimental    = %.5f (teorica 0.5)%n", media(u));
        System.out.printf(Locale.US, "Varianza experimental = %.5f (teorica %.5f)%n", varianza(u), 1.0 / 12);
        return u;
    }

    // ---------- 2. Transformada inversa ----------
    static double[] transformadaInversa(double[] u, double lambda) {
        if (lambda <= 0) throw new IllegalArgumentException("lambda debe ser > 0");
        double[] x = new double[u.length];
        for (int i = 0; i < u.length; i++) x[i] = -Math.log(1.0 - u[i]) / lambda;
        return x;
    }

    // ---------- 3. Histograma + densidad teórica (CSV para graficar) ----------
    static void histogramaCSV(double[] x, double lambda, int bins, String ruta) throws IOException {
        double max = 0;
        for (double d : x) max = Math.max(max, d);
        double ancho = max / bins;
        int[] cuenta = new int[bins];
        for (double d : x) {
            int k = (int) (d / ancho);
            if (k >= bins) k = bins - 1;
            cuenta[k]++;
        }
        try (PrintWriter pw = new PrintWriter(new FileWriter(ruta))) {
            pw.println("centro_bin,densidad_empirica,densidad_teorica");
            for (int k = 0; k < bins; k++) {
                double centro = (k + 0.5) * ancho;
                double emp = cuenta[k] / (x.length * ancho);
                double teo = lambda * Math.exp(-lambda * centro);
                pw.printf(Locale.US, "%.5f,%.6f,%.6f%n", centro, emp, teo);
            }
        }
    }

    public static void main(String[] args) throws IOException {
        Random rnd = new Random(SEMILLA);
        double[] u = generarUniformes(N, rnd);

        System.out.println("\n=== 2. TRANSFORMADA INVERSA (lambda = " + LAMBDA_BASE + ") ===");
        double[] x = transformadaInversa(u, LAMBDA_BASE);
        System.out.println("Primeros 10 valores:");
        for (int i = 0; i < 10; i++)
            System.out.printf(Locale.US, "  X[%2d] = %.5f (U = %.5f)%n", i + 1, x[i], u[i]);
        System.out.println("Cantidad de datos generados: " + x.length);

        histogramaCSV(x, LAMBDA_BASE, 50, "../resultados/java_histograma_lambda_0.5.csv");

        // ---------- 4 y 5. Estadísticas por lambda ----------
        System.out.println("\n=== 4/5. COMPARACION DE MEDIDAS ESTADISTICAS ===");
        System.out.printf("%-7s %-11s %-11s %-9s %-11s %-11s %-9s%n",
                "lambda", "Media teo", "Media exp", "Err% med", "Var teo", "Var exp", "Err% var");
        try (PrintWriter pw = new PrintWriter(new FileWriter("../resultados/java_tabla_comparativa.csv"))) {
            pw.println("lambda,media_teorica,media_experimental,error_media_pct,"
                    + "varianza_teorica,varianza_experimental,error_varianza_pct");
            for (double lam : TASAS) {
                double[] xi = transformadaInversa(u, lam);
                double mT = 1.0 / lam, vT = 1.0 / (lam * lam);
                double mE = media(xi), vE = varianza(xi);
                double eM = Math.abs(mE - mT) / mT * 100, eV = Math.abs(vE - vT) / vT * 100;
                System.out.printf(Locale.US, "%-7.1f %-11.5f %-11.5f %-9.4f %-11.5f %-11.5f %-9.4f%n",
                        lam, mT, mE, eM, vT, vE, eV);
                pw.printf(Locale.US, "%.1f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f%n",
                        lam, mT, mE, eM, vT, vE, eV);
            }
        }
    }
}
