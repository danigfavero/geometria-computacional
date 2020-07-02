#!/usr/bin/env python
"""Computa o fecho convexo 2D de uma coleção de n pontos, usando uma técnica de
divisão e conquista similar ao Quicksort."""

from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.prim import right, area2, left, collinear, dist2

# coleções globais auxiliando a animação :p
ids = []
points = {}

def area(a, b, c):
    '''Devolve a área do triângulo cujos extremos são os pontos a, b, c.'''
    return abs(area2(a, b, c)/2.0)

def extreme(P, p, r):
    '''Recebe P e, usando area, devolve o índice de um ponto extremo da coleção
    distinto de p e r.'''
    q = p + 1
    greatest = area(P[p], P[r], P[q])
    for i in range(p + 2, r):
        a = area(P[p], P[r], P[i])
        if a > greatest:
            q = i
            greatest = a
        # desempata pegando o ponto mais alto (ou mais à esquerda)
        elif a == greatest:
            if P[i].y > P[q].y or (P[i].y == P[q].y and P[i].x > P[q].x):
                q = i
                greatest = a

    return q

def partition(P, p, r):
    '''Recebe uma coleção de pontos em posição geral, com pelo menos 3 pontos tal
    que os pontos de índice p e r são extremos consecutivos na fronteira do fecho
    convexo da coleção no sentido anti-horário. Rearranja a coleção de pontos e
    devolve (s,q) para o algoritmo do QuickHull.'''
    q = extreme(P, p, r)
    P[p + 1], P[q] = P[q], P[p + 1]
    s = q = r

    for point, id in ids:
        point.unhilight(id)

    for k in range(r - 1, p, -1):
        if left(P[p], P[p + 1], P[k]):
            id = P[k].hilight('green')
            ids.append((P[k], id))
            s -= 1
            P[s], P[k] = P[k], P[s]
        elif left(P[p + 1], P[r], P[k]):
            id = P[k].hilight('red')
            ids.append((P[k], id))
            s -= 1
            q -= 1
            P[k], P[q] = P[q], P[k]
            if s != q:
                P[k], P[s] = P[s], P[k]

    control.thaw_update()
    control.update()
    control.freeze_update()
    control.sleep()

    s -= 1
    q -= 1
    P[q], P[p + 1] = P[p + 1], P[q]

    if s != q:
        P[s], P[p + 1] = P[p + 1], P[s]
    s -= 1
    P[s], P[p] = P[p], P[s]
    return s, q

def quickhull_rec(P, p, r):
    '''Miolo recursivo da função Quickhull. Recebe uma coleção de pontos P, um
    início p e um fim r dados por meio da função partition. Devolve os hulls
    gerados a cada chamada recursiva.'''
    if p == r - 1:
        P[r].lineto(P[p], 'cyan')
        control.thaw_update()
        control.update()
        control.freeze_update()
        control.sleep()
        return [P[r], P[p]]

    if (P[p], P[r]) in points.keys():
        id = points.pop((P[p], P[r]))
        control.plot_delete(id)

    s, q = partition(P, p, r)

    points[(P[p], P[q])] = P[p].lineto(P[q], 'cyan')
    points[(P[q], P[r])] = P[q].lineto(P[r], 'cyan')
    control.thaw_update()
    control.update()
    control.freeze_update()
    control.sleep()

    hull = quickhull_rec(P, q, r)
    hull2 = quickhull_rec(P, s, q)
    print("1: ", hull)
    print("2: ", hull2)
    # junta os hulls e remove uma cópia do q
    for i in range(1, len(hull2)):
        hull.append(hull2[i])
    print("1 + 2: ", hull)
    return hull

def Quickhull(P):
    '''Recebe uma coleção de pontos P e devolve seu fecho convexo'''
    n = len(P)
    if n == 1:
        return [P[0]]

    # encontra primeiro ponto extremo
    k = 0
    for i in range(n):
        # desempata por x
        if P[i].y < P[k].y or (P[i].y == P[k].y and P[i].x < P[k].x):
            k = i
    P[0], P[k] = P[k], P[0]

    # encontra extremo consecutivo ao primeiro
    i = 1
    dist = 0
    for j in range(2, n):
        if right(P[0], P[i], P[j]):
            i = j
        # desempata pelo mais distante
        elif collinear(P[0], P[i], P[j]) and dist2(P[0], P[i]) < dist2(P[0], P[j]):
            i = j
    P[n - 1], P[i] = P[i], P[n - 1]

    P[0].lineto(P[n-1], 'cyan')
    control.thaw_update()
    control.update()
    control.freeze_update()
    control.sleep()
    quick = quickhull_rec(P, 0, n-1)
    #print(quick)
    return quick

