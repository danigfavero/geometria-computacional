import math

###########mergesort carinhosamente inspirado pela internet############# 
# valeu, jayesh do https://rextester.com/PEAA86258
def merge(left, right):
    leftIndex = 0
    rightIndex = 0
    
    result = []
    
    while leftIndex < len(left) and rightIndex < len(right):
        if left[leftIndex] <= right[rightIndex]:
            result.append(left[leftIndex])
            leftIndex += 1
        else:
            result.append(right[rightIndex])
            rightIndex += 1
    
    if leftIndex < len(left):
        result.extend(left[leftIndex:])
    elif rightIndex < len(right):
        result.extend(right[rightIndex:])
        
    return result
    
def merge_sort(xarr, yarr):
    if xarr is None:
        return None
    
    if len(xarr) < 2:
        return xarr, yarr
    
    xleft = xarr[: len(xarr) // 2]
    yleft = yarr[: len(xarr) // 2]
    xright = xarr[len(xarr) // 2 :]
    yright = yarr[len(xarr) // 2 :]
    
    return merge(merge_sort(xleft, yleft), merge_sort(xright, y))

def merge_sort_ind():
    pass

def distancia_sh(X, Y, n):
    merge_sort(X, Y, 1, n)
    a = [i for i in range(1, n)]
    merge_sort_ind(Y, 1, n, a) # ordenação indireta
    return distancia_rec_sh(X, Y, a, 1, n)

def distancia_rec_sh(X, Y, a, p, r):
    if r <= p + 2:
        pass # resolva o problema diretamente
    else:
        q = (p + r)//2
        b = divida(X, Y, a, p, r)
        de = distancia_rec_sh(X, Y, b, p, q)
        dd = distancia_rec_sh(X, Y, b, q + 1, r)
        return combine(X, Y, a, p, r, de, dd)

def divida(X, Y, a, p, r):
    q = (p + r) // 2
    i = p - 1
    j = q
    b = [0 for i in range(r - p)] # certeza?
    for k in range (p, r):
        if a[k] <= p: # (X[a[k]], Y [a[k]]) está à esquerda da reta x = X[q]?
            i += 1
            b[i] = a[k]
        else:
            j += 1
            b[j] = a[k]
    return b

def candidatos(X, a, p, r, d):
    q = (p + r) // 2
    t = 0
    f = [0 for i in range(r - p)] # certeza?
    for k in range(p, r):
        if abs(X[a[k]] - X[q]) < d:
            t += 1
            f[t] = a[k]
    return f,t

def combine(X, Y, a, p, r, de, dd):
    d = min(de,dd)
    (f,t) = candidatos(X, a, p, r, d)
    for i in range(1, t-1):
        for j in range(i+1, min(i+7, t)):
            dlinha = distancia(X[f[i]], Y[f[i]], X[f[j]], Y[f[j]])
            if dlinha < d:
                d = dlinha
    return d

def distancia(xa, ya, xb, yb):
    return math.sqrt((xb - xa)**2 + (yb - ya)**2)

def main():
    n = int(input())
    while n != 0:
        X = []
        Y = []
        for i in range(n):
            coord = input().split
            X.append(int(coord[0]))
            Y.append(int(coord[1]))
        print(distancia_sh(X, Y, n))
        n = int(input())
