from geocomp.common.point import Point
from geocomp.common.polygon import Polygon
from geocomp.common import control
from geocomp.common.guiprim import *

def area2(a, b, c):
    '''Recebe 3 pontos e devolve a área do polígono delimitado pelos pontos
    multiplicada por 2'''
    return (a.x - c.x)*(b.y - c.y) - (a.y - c.y)*(b.x - c.x)

def left_plus(a, b, c):
    '''Verifica se o ponto c está à esquerda da reta dada por ab'''
    return area2(a, b, c) > 0

def left(a, b, c):
    '''Verifica se o ponto c está à esquerda ou sobre a reta dada por ab'''
    return area2(a, b, c) >= 0

def collinear(a, b, c):
    '''Verifica se os pontos a, b, c são colineares'''
    return area2(a, b, c) == 0

def is_crescent(i, j, k):
    '''Verifica se os valor i, j, k estão em ordem não descrescente'''
    return i <= j and j <= k

def between(a, b, c):
    '''Verifica se o ponto c está no segmento ab'''
    if not collinear(a, b, c):
        return False
    if a.x != b.x:
        return is_crescent(a.x, c.x, b.x) or is_crescent(a.x, c.x, b.x)
    return is_crescent(a.y, c.y, b.y) or is_crescent(a.y, c.y, b.y)

def intersects_prop(a, b, c, d):
    '''Verifica se os segmentos ab e cd se intersectam propriamente'''
    if collinear(a, b, c) or collinear(a, b, d) or collinear(c, d, a) or collinear(c, d, b):
        return False
    return (left_plus(a, b, c) ^ left_plus(a, b, d)) and (left_plus(c, d, a) ^ left_plus(c, d, b))

def intersects(a, b, c, d):
    '''Verifica se os segmentos ab e cd se intersectam propriamente'''
    if intersects_prop(a, b, c, d):
        return True
    return between(a, b, c) or between(a, b, d) or between(c, d, a) or between(c, d, b)

def in_cone(P, u, w):
    '''Verifica se o segmento uw está no cone das arestas vizinhas do polígono'''
    v = P.prev(u)
    t = P.next(v)
    if left(v, u, t):
        return left_plus(u, w, v) and left_plus(w, u, t)
    return left(u, w, t) and left(w, u, v)

def almost_diagonal(P, u, w):
    '''Decide se dois vértices u, w de um polígono P formam uma quase-diagonal,
    ou seja, ignorando o caso do segmento uw estar no cone das arestas vizinhas
    do polígono'''
    v = P.head()
    t = P.next(v)
    while True:
        if (v != u) and (v != w) and (t != u) and (t != w):
            if intersects(u, w, v, t):
                return False
        if t == P.head():
            return True
        v = t
        t = P.next(v)

def diagonal(P, u, w):
    '''Decide se dois vértices u, w de um polígono P formam uma diagonal'''
    return in_cone(P, u, w) and almost_diagonal(P, u, w)

def ear_tip(P, v):
    '''Recebe um polígono P e um vértice v desse polígono, e decide se ele é
    uma ponta de orelha'''
    u = P.prev(v)
    w = P.next(v)
    v.hilight('green')
    u.hilight('yellow')
    w.hilight('yellow')
    control.update()
    diag = diagonal(P, u, w)
    u.unhilight()
    w.unhilight()
    if not diag:
        v.unhilight()
    control.update()
    return diag

def find_ears(P):
    '''Recebe um polígono P e devolve um dicionário cujas chaves são pontos e
    os valores dizem se os pontos correspondentes são pontas de orelha ou não'''
    ears = {}
    v = P.head()
    while True:
        ears[v] = ear_tip(P,v)
        v = P.next(v)
        if v == P.head():
            break
    return ears

def triangulation(n, P):
    '''Recebe um polígono P com n lados e devolve a triangulação de P'''
    ears = find_ears(P)
    v3 = P.head()
    while n > 3:
        v2 = v3
        while not ears[v2]:
            v2 = P.next(v2)
        v2.hilight("blue")
        v1 = P.prev(v2)
        v3 = P.next(v2)
        v1.lineto(v3, "blue")
        control.update()
        print(v1, v3)
        v2.unhilight()
        control.update()
        P.remove_vertex(v2)
        n -= 1
        ears[v1] = ear_tip(P, v1)
        ears[v3] = ear_tip(P, v3)

def Ear_clipping(lista):
    P = lista[0]
    n = len(P.vertices())
    triangulation(n, P)
