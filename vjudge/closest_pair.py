import math

def distancia_sh(X, Y, n):
    zipado = list(zip(X,Y))
    zipado2 = sorted(zipado)
    deszipado = list(zip(*zipado2))
    return distancia_rec_sh(list(deszipado[0]), list(deszipado[1]), 1, n)

def distancia_rec_sh(X, Y, p, r):
    if r <= p + 2:
        return brute_force(X, Y, p, r)
    q = (p + r)//2
    de = distancia_rec_sh(X, Y, p, q)
    dd = distancia_rec_sh(X, Y, q + 1, r)
    intercale(X, Y, p, q, r)
    return combine(X, Y, p, r, de, dd)

def brute_force(X, Y, p, r):
    dist = 10000
    X2 = X[p:r+1]
    Y2 = Y[p:r+1]
    zipado = list(zip(X2,Y2))
    zipado2 = sorted(zipado, key=lambda x:x[1])
    deszipado = list(zip(*zipado2))
    X2 = list(deszipado[0])
    Y2 = list(deszipado[1])

    for i in range(p, r+1):
        X[i] = X2[i-p]
        Y[i] = Y2[i-p]

    for i in range(p, r+1):
        for j in range(i+1, r+1):
            aux = distancia(X[i], Y[i], X[j], Y[j])
            if aux < dist:
                dist = aux
    return dist

def distancia(xa, ya, xb, yb):
    return math.sqrt((xb - xa)**2 + (yb - ya)**2)

def intercale(X, Y, p, q, r):
    i = p 
    j = q + 1
    X2 = []
    Y2 = []
    while i <= q and j <= r:

        while i <= q and Y[i] <= Y[j]:
            X2.append(X[i])
            Y2.append(Y[i])
            i += 1

        while j <= r and Y[j] <= Y[i]:
            X2.append(X[j])
            Y2.append(Y[j])
            j += 1
    
    while i <= q:
        X2.append(X[i])
        Y2.append(Y[i])
        i += 1

    while j <= r:
        X2.append(X[j])
        Y2.append(Y[j])
        j += 1
    
    for i in range(p, r+1):
        X[i] = X[i-p]
        Y[i] = Y[i-p]

def combine(X, x, Y, p, r, de, dd):
    d = min(de,dd)
    (f,t) = candidatos(X, x, p, r, d)
    for i in range(1, t-1):
        for j in range(i+1, min(i+7, t)):
            dlinha = distancia(X[f[i]], Y[f[i]], X[f[j]], Y[f[j]])
            if dlinha < d:
                d = dlinha
    return d

def candidatos(X, x, p, r, d):
    q = (p + r) // 2
    t = 0
    f = [0 for i in range(p, r+1)]
    for k in range(p, r+1):
        if abs(x - X[k]) < d:
            f[t] = X[k]
            t += 1
    return f, t

def main():
    n = int(input())
    while n != 0:
        X = []
        Y = []
        for i in range(n):
            coord = input().split()
            X.append(int(coord[0]))
            Y.append(int(coord[1]))
        d = distancia_sh(X, Y, n)
        if d > 10000:
            print("INFINITY")
        else:    
            print(d)
        n = int(input())

main()
