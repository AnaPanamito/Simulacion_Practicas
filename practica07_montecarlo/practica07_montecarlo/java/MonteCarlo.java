import java.io.IOException;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Locale;
import java.util.Random;

/**
 * Práctica Nro. 07 - Simulación (UNL, Carrera de Computación)
 * Estimación de π mediante el método de Monte Carlo (implementación en Java).
 *
 * Compilar: javac MonteCarlo.java
 * Ejecutar: java MonteCarlo [ruta_csv]
 */
public class MonteCarlo {

    private static final long SEMILLA = 42L;                       // semilla fija
    private static final int[] TAMANOS = {1_000, 10_000, 100_000, 1_000_000};
    private static final int REPETICIONES = 5;                     // para la mediana del tiempo
    private static final int CALENTAMIENTO = 5;                    // pasadas para que el JIT optimice

    /** Genera N puntos en [-1,1]x[-1,1] y devuelve Nc (puntos con x²+y² ≤ 1). */
    static long contarDentro(int n, long semilla) {
        Random rnd = new Random(semilla);
        long nc = 0;
        for (int i = 0; i < n; i++) {
            double x = 2.0 * rnd.nextDouble() - 1.0;   // x en [-1, 1)
            double y = 2.0 * rnd.nextDouble() - 1.0;   // y en [-1, 1)
            if (x * x + y * y <= 1.0) {
                nc++;
            }
        }
        return nc;
    }

    public static void main(String[] args) throws IOException {
        // Fuerza UTF-8 en consola para mostrar correctamente el símbolo π
        System.setOut(new PrintStream(System.out, true, java.nio.charset.StandardCharsets.UTF_8));
        String ruta = args.length > 0 ? args[0] : Paths.get("..", "resultados", "resultados_java.csv").toString();

        // Calentamiento (no se registra): la JVM compila a código nativo (JIT) tras varias pasadas.
        for (int i = 0; i < CALENTAMIENTO; i++) {
            contarDentro(200_000, SEMILLA);
        }

        StringBuilder csv = new StringBuilder("N,pi_estimado,error_absoluto,tiempo_s\n");
        System.out.println("=".repeat(68));
        System.out.printf(Locale.US, " Monte Carlo (Java) | java.util.Random | semilla=%d%n", SEMILLA);
        System.out.printf(Locale.US, " π real = %.10f | tiempo = mediana de %d ejecuciones%n", Math.PI, REPETICIONES);
        System.out.println("=".repeat(68));
        System.out.printf(Locale.US, "%12s | %12s | %12s | %11s%n", "N", "π estimado", "Error abs.", "Tiempo (s)");
        System.out.println("-".repeat(68));

        for (int n : TAMANOS) {
            double[] tiempos = new double[REPETICIONES];
            long nc = 0;
            for (int r = 0; r < REPETICIONES; r++) {
                long t0 = System.nanoTime();                 // inicio: SOLO generación + clasificación
                nc = contarDentro(n, SEMILLA);
                long t1 = System.nanoTime();                 // fin
                tiempos[r] = (t1 - t0) / 1e9;                // nanosegundos -> segundos
            }
            Arrays.sort(tiempos);
            double tiempo = tiempos[REPETICIONES / 2];       // mediana

            double piEst = 4.0 * nc / n;                     // π ≈ 4 · (Nc / N)
            double error = Math.abs(piEst - Math.PI);        // error absoluto

            System.out.printf(Locale.US, "%,12d | %12.6f | %12.6f | %11.6f%n", n, piEst, error, tiempo);
            csv.append(String.format(Locale.US, "%d,%.10f,%.10f,%.6f%n", n, piEst, error, tiempo));
        }
        System.out.println("-".repeat(68));

        Path p = Paths.get(ruta);
        if (p.getParent() != null) Files.createDirectories(p.getParent());
        try (PrintWriter pw = new PrintWriter(Files.newBufferedWriter(p))) {
            pw.print(csv);
        }
        System.out.println("CSV guardado en: " + ruta);
    }
}
