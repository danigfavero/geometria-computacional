#!/usr/bin/env python
"""Computa o fecho convexo 2D de uma coleção de n pontos, usando uma técnica
de divisão e conquista similar ao Quicksort."""

from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.prim import right, area2, left


def area(a, b, c):
    '''Devolve a área do triângulo cujos extremos são os pontos a, b, c.'''
    return abs(area2/2.0)

def extreme(P, p, r):
    '''Recebe P e, usando area, devolve o índice de um ponto extremo da coleção
    distinto de p e r.'''
    q = p + 1
    larger = area(P[p], P[r], P[q])
    for i in range(p + 2, r - 1):
        if area(P[p], P[r], P[i]) > larger:
            q = i
            larger = area(P[p], P[r], P[q])
    return q

def partition(P, p, r):
    '''Recebe uma coleção de pontos em posição geral, com pelo menos 3 pontos
    tal que os pontos de índice p e r são extremos consecutivos na fronteira do
    fecho convexo da coleção no sentido anti-horário. Rearranja a coleção de
    pontos e devolve (s,q) para o algoritmo do QuickHull.'''
    q = extreme(P, p, r)
    P[p + 1], P[q] = P[q], P[p + 1]
    s = q = r

    for k in range(r - 1, p + 2, -1):
        if left(P[p], P[p + 1], P[k]):
            s -= 1
            P[s], P[k] = P[k], P[s]
        elif left(P[p + 1], P[r], P[k]):
            s -= 1
            q -= 1
            P[k], P[q] = P[q], P[k]
            if s != q:
                P[k], P[s] = P[s], P[k]
    s -= 1
    q -= 1
    P[q], P[p + 1] = P[p + 1], P[q]

    if s != q:
        P[s], P[p + 1] = P[p + 1], P[s]
    p -= 1
    P[s], P[p] = P[p], P[s]
    return s, q

def quickhull_rec(P, p, r):
    '''Miolo recursivo da função Quickhull. Recebe uma coleção de pontos P, um
    início p e um fim r dados por meio da função partition. Devolve os hulls
    gerados a cada chamada recursiva.'''
    if p == r - 1:
        return [P[r], P[p]]

    s, q = partition(P, p, r)
    hull = quickhull_rec(P, q, r)
    hull2 = quickhull_rec(P, s, q)

    h = len(hull)
    for i in range(1, len(hull2)):
        hull[h] = hull2[i]
        h += 1
    return hull

def Quickhull(P):
    '''Recebe uma coleção de pontos P e devolve seu fecho convexo'''
    n = len(P)
    if n == 1:
        return [P[0]]

    k = 0
    for i in range(n):
        if P[i].y < P[k].y:
            k = i
    P[0], P[k] = P[k], P[0]

    i = 1
    for j in range(2, n):
        if right(0, P[i], P[j]):
            i = j
    P[n], P[i] = P[i], P[n]

    return quickhull_rec(P, 0, n-1)
