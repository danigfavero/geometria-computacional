from geocomp.common.point import Point
from geocomp.common.polygon import Polygon

def area2(a, b, c):
    return (a.x - c.x)*(b.y - c.y) - (a.y - c.y)*(b.x - c.x)

def left_plus(a, b, c):
    return area2(a, b, c) > 0

def left(a, b, c):
    return area2(a, b, c) >= 0

def collinear(a, b, c):
    return area2(a, b, c) == 0

def is_crescent(i, j, k):
    return i <= j and j <= k

def between(a, b, c):
    if not collinear(a, b, c):
        return False
    if a.x != b.x:
        return is_crescent(a.x, c.x, b.x) or is_crescent(a.x, c.x, b.x)
    return is_crescent(a.y, c.y, b.y) or is_crescent(a.y, c.y, b.y)

def intersects_prop(a, b, c, d):
    if collinear(a, b, c) or collinear(a, b, d) or collinear(c, d, a) or collinear(c, d, b):
        return False
    return (left_plus(a, b, c) ^ left_plus(a, b, d)) and (left_plus(c, d, a) ^ left_plus(c, d, b))

def intersects(a, b, c, d):
    if intersects_prop(a, b, c, d):
        return True
    return between(a, b, c) or between(a, b, d) or between(c, d, a) or between(c, d, b)

def in_cone(n, P, i, j):
    u = (i - 1) % n
    w = (i + 1) % n
    if left(P[u], P[i], P[w]):
        return left_plus(P[i], P[j], P[u]) and left_plus(P[j], P[i], P[w])
    return left(P[i], P[j], P[w]) and left(P[j], P[i], P[u])

def almost_diagonal(n, P, i, j):
    for k in range(0, n-1):
        l = (k + 1) % n
        if (k != i) and (k != j) and (l != i) and (l != j):
            if intersects(P[i], P[j], P[k], P[l]):
                return False
    return True

def diagonal(n, P, i, j):
    return in_cone(n, P, i, j) and almost_diagonal(n, P, i, j)

def ear_tip(n, P, i):
    j = (i - 1) % n
    k = (i + 1) % n
    return diagonal(n, P, j, k)

def check_ear(P):
    v = 0 # TODO como inicializar?
    while v != P:
        v = P
        u = prev[v]
        w = prev[v]
        ear[v] = diagonal(P, u, w)
        v = w

def triangulation(n, P):
    check_ear(P)
    while n > 3:
        v2 = P
        while not ear[v2]:
            v2 = nextt[v2]
        v1 = prev[v2]
        v3 = nextt[v2]
        print((vert[v1], vert[v3]))
        nextt[v1] = v3
        prev[v3] = v1
        P = v3
        n -= 1
        ear[v1] = ear_tip(P, v1)
        ear[v3] = ear_tip(P, v3)