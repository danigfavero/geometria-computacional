import java.util.Scanner; 
import java.lang.Math;
import java.util.Arrays;
import java.util.Comparator;

public class ClosestPair {

    public double dist;

    public ClosestPair(Ponto[] pontos, int n) {
        Arrays.sort(pontos, Ponto.X_ORDER);
        dist = Math.sqrt(distanciaRecSH(pontos, 0, n-1));
    }

    private double distanciaRecSH(Ponto[] pontos, int p, int r) {
        if (r <= p + 2) {
            return forcaBruta(pontos, p, r);
        }
        int q = (int) Math.floor((p + r)/2);
        double de = distanciaRecSH(pontos, p, q);
        double dd = distanciaRecSH(pontos, q + 1, r);
        intercale(pontos, p, q, r);
        return combine(pontos, pontos[q].x, p, r, de, dd);
    }

    private double forcaBruta(Ponto[] pontos, int p, int r) {
        double dist2 = 100000000;
        Ponto[] brute = slice(pontos, p, r+1);
        Arrays.sort(brute, Ponto.Y_ORDER);

        for (int i = p; i < r+1; i++) {
            pontos[i] = brute[i-p];
        }

        for (int i = p; i < r+1; i++) {
            for (int j = i+1; j < r+1; j++) {
                double aux = pontos[i].distancia2(pontos[j]);
                if (aux < dist2) {
                    dist2 = aux;
                }
            }
        }
        return dist2;
        
    }

    private static Ponto[] slice(Ponto[] arr, int start, int end) { 
        Ponto[] slice = new Ponto[end - start]; 
        for (int i = 0; i < slice.length; i++) { 
            slice[i] = arr[start + i]; 
        } 
        return slice; 
    } 

    private void intercale(Ponto[] pontos, int p, int q, int r) {
        int i = p; 
        int j = q + 1;
        Ponto[] intercalado = new Ponto[r - p + 1];
        int k = 0;

        while (i <= q && j <= r) {
            while (i <= q && pontos[i].y <= pontos[j].y) {
                intercalado[k++] = pontos[i++];
            }
        
            while (j <= r && pontos[j].y <= pontos[i].y) {
                intercalado[k++] = pontos[j++];
            }
        }

        while (i <= q) {
            intercalado[k++] = pontos[i++];
        }
        while (j <= r) {
            intercalado[k++] = pontos[j++];
        }

        for (i = p; i < r+1; i++) {
            pontos[i] = intercalado[i-p];
        }
    }

    private double combine(Ponto[] pontos, double x, int p, int r, double de, double dd) {
        double d = Math.min(de, dd);
        int[] ref = new int[1];
        Ponto[] f = new Ponto[r+1 - p];
        f = candidatos(pontos, x, p, r, d, ref);
        int t = ref[0];
        for (int i = 0; i < t; i++) {
            for (int j = i+1; j < Math.min(i+7, t); j++) {
                double dlinha = f[i].distancia2(f[j]);
                if (dlinha < d) {
                    d = dlinha;
                }
            }
        }
        return d;
    }

    private Ponto[] candidatos(Ponto[] pontos, double x, int p, int r, double d, int[] ref) {
        int t = 0;
        Ponto[] f = new Ponto[r+1 - p];
        for (int k = p; k < r+1; k++) {
            if (Math.abs(x - pontos[k].x) * Math.abs(x - pontos[k].x) < d) {
                f[t] = pontos[k];
                t++;
            }    
        }
        ref[0] = t;
        
        return f;
    }

    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = Integer.parseInt(s.nextLine());
        while (n != 0) {
            Ponto pontos[] = new Ponto[n];
            for (int i = 0; i < n; i++) {
                String[] coord = s.nextLine().split(" "); 
                Ponto ponto = new Ponto(Double.parseDouble(coord[0]), Double.parseDouble(coord[1]));
                pontos[i] = ponto;
            }
            double d = (new ClosestPair(pontos, n)).dist;
            if (d >= 10000) {
                System.out.println("INFINITY");
            } else {
                System.out.println(d);
            }
            n = Integer.parseInt(s.nextLine());
        }
    }
}

class Ponto implements Comparable<Ponto> {

    public double x;
    public double y;
    public static final Comparator<Ponto> X_ORDER = new XOrder();
    public static final Comparator<Ponto> Y_ORDER = new YOrder();

    public Ponto(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double distancia2(Ponto other) {
        return Math.pow(this.x - other.x, 2) + Math.pow(this.y - other.y, 2);
    }

    public int compareTo(Ponto that) {
        if (this.x < that.x) return -1;
        if (this.x > that.x) return +1;
        if (this.y < that.y) return -1;
        if (this.y > that.y) return +1;
        return 0;
    }

    private static class YOrder implements Comparator<Ponto> {
        public int compare(Ponto p, Ponto q) {
            if (p.y < q.y) return -1;
            if (p.y > q.y) return +1;
            return 0;
        }
    }

    private static class XOrder implements Comparator<Ponto> {
        public int compare(Ponto p, Ponto q) {
            return p.compareTo(q);
        }
    }
}

class WrapInt {
    public int value;
}