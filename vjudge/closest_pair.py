from math import sqrt

def distancia_sh(pontos, n):
    pontos.sort(key=lambda x:x[0])
    return sqrt(distancia_rec_sh(pontos, 0, n-1))

def distancia_rec_sh(pontos, p, r):
    if r <= p + 2:
        return forca_bruta(pontos, p, r)
    q = (p + r)//2
    de = distancia_rec_sh(pontos, p, q)
    dd = distancia_rec_sh(pontos, q + 1, r)
    intercale(pontos, p, q, r)
    return combine(pontos, pontos[q][0], p, r, de, dd)

def forca_bruta(pontos, p, r):
    dist2 = 100000000
    brute = pontos[p:r+1]
    brute.sort(key=lambda x:x[1])

    for i in range(p, r+1):
        pontos[i] = brute[i-p]

    for i in range(p, r+1):
        for j in range(i+1, r+1):
            aux = distancia2(pontos[i], pontos[j])
            if aux < dist2:
                dist2 = aux
    return dist2

def distancia2(a, b):
    return (b[0] - a[0])**2 + (b[1] - a[1])**2

def intercale(pontos, p, q, r):
    i = p 
    j = q + 1
    intercalado = []

    while i <= q and j <= r:
        while i <= q and pontos[i][1] <= pontos[j][1]:
            intercalado.append(pontos[i])
            i += 1

        while j <= r and pontos[j][1] <= pontos[i][1]:
            intercalado.append(pontos[j])
            j += 1
    
    while i <= q:
        intercalado.append(pontos[i])
        i += 1

    while j <= r:
        intercalado.append(pontos[j])
        j += 1
    
    for i in range(p, r+1):
        pontos[i] = intercalado[i-p]

def combine(pontos, x, p, r, de, dd):
    d = min(de,dd)
    (f,t) = candidatos(pontos, x, p, r, d)
    for i in range(t):
        for j in range(i+1, min(i+7, t)):
            dlinha = distancia2(f[i], f[j])
            if dlinha < d:
                d = dlinha
    return d

def candidatos(pontos, x, p, r, d):
    t = 0
    f = []
    for k in range(p, r+1):
        if abs(x - pontos[k][0]) * abs(x - pontos[k][0]) < d:
            f.append(pontos[k])
            t += 1
    return f, t

def main():
    n = int(input())
    while n != 0:
        pontos = []
        for i in range(n):
            coord = input().split()
            x = int(coord[0])
            y = int(coord[1])
            pontos.append((x,y))
        d = distancia_sh(pontos, n)
        if d >= 10000:
            print("INFINITY")
        else:    
            print(format(d, '.4f'))
        n = int(input())

main()
