from math import sqrt

def distancia_sh(points, n):
    points.sort(key=lambda x:x[0])
    return sqrt(distancia_rec_sh(points, 0, n-1))

def distancia_rec_sh(points, p, r):
    if r <= p + 2:
        return brute_force(points, p, r)
    q = (p + r)//2
    de = distancia_rec_sh(points, p, q)
    dd = distancia_rec_sh(points, q + 1, r)
    intercale(points, p, q, r)
    return combine(points, points[q][0], p, r, de, dd)

def brute_force(points, p, r):
    dist = 10000.0 ** 2
    brute = points[p:r+1]
    brute.sort(key=lambda x:x[1])

    for i in range(p, r+1):
        points[i] = brute[i-p]

    for i in range(p, r+1):
        for j in range(i+1, r+1):
            aux = distancia2(points[i], points[j])
            if aux < dist:
                dist = aux
    return dist

def distancia2(a, b):
    return (b[0] - a[0])**2 + (b[1] - a[1])**2

def intercale(points, p, q, r):
    i = p 
    j = q + 1
    intercalado = []

    while i <= q and j <= r:
        while i <= q and points[i][1] <= points[j][1]:
            intercalado.append(points[i])
            i += 1

        while j <= r and points[j][1] <= points[i][1]:
            intercalado.append(points[j])
            j += 1
    
    while i <= q:
        intercalado.append(points[i])
        i += 1

    while j <= r:
        intercalado.append(points[j])
        j += 1
    
    for i in range(p, r+1):
        points[i] = intercalado[i-p]

def combine(points, x, p, r, de, dd):
    d = min(de,dd)
    (f,t) = candidatos(points, x, p, r, d)
    for i in range(t):
        for j in range(i+1, min(i+7, t)):
            dlinha = distancia2(f[i], f[j])
            if dlinha < d:
                d = dlinha
    return d

def candidatos(points, x, p, r, d):
    t = 0
    f = [0 for i in range(p, r+1)]
    for k in range(p, r+1):
        if abs(x - points[k][0]) < d:
            f[t] = points[k]
            t += 1
    return f, t

def main():
    n = int(input())
    while n != 0:
        points = []
        for i in range(n):
            coord = input().split()
            x = int(coord[0])
            y = int(coord[1])
            points.append((x,y))
        d = distancia_sh(points, n)
        if d >= 10000:
            print("INFINITY")
        else:    
            print(d)
        n = int(input())

main()
