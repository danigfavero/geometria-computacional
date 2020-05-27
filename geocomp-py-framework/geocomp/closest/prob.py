#!/usr/bin/env python
"""Algoritmo aleatorizado"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
import math
from random import shuffle

def square_id(p, delta, offset):
    """ Função que recebe um ponto, a distância mínima dessa iteração (delta)
    e um offset; devolvendo o identificador do quadrado no qual o ponto está
    """
    aux = math.sqrt(delta)
    return math.floor((2*(p.x + offset))/aux), math.floor((2*(p.y+offset))/aux)

def Prob (l):
    """Algoritmo probabilístico para encontrar o par de pontos mais próximo
    """
    if len(l) < 2:
        return None
    shuffle(l)
    
    offset = float("inf")
    for p in l:
        offset = min(offset, p.x, p.y)
    offset = min(0, offset)
    
    delta = dist2(l[0], l[1])
    S = {}
    S[square_id(l[0], delta, offset)] = 0
    S[square_id(l[1], delta, offset)] = 1
    a = l[0]
    b = l[1]

    control.freeze_update()
    hia = a.hilight()
    hib = b.hilight()
    id = a.lineto(b)
    control.thaw_update() 
    control.update()

    for i in range(2, len(l)):
        current_id = square_id(l[i], delta, offset)
        update = False

        for u in range(-2, 3):
            for v in range(-2, 3):
                next = (current_id[0] + u, current_id[1] + v)
                if next in S:
                    dist = dist2(l[S[next]], l[i])
                    if dist < delta:
                        delta = dist

                        update = True
                        control.freeze_update()
                        if a != None:
                            a.unhilight(hia)
                        if b != None:
                            b.unhilight(hib)
                        if id != None:
                            control.plot_delete(id)

                        a = l[i]
                        b = l[S[next]]

                        hia = a.hilight()
                        hib = b.hilight()
                        id = a.lineto(b)
                        control.thaw_update() 
                        control.update()

        if delta == 0:
            break

        if update:
            S.clear()
            for j in range(0, i + 1):
                S[square_id(l[j], delta, offset)] = j
        else:
            S[current_id] = i

    a.hilight('green')
    b.hilight('green')
    ret = Segment(a, b)
    ret.extra_info = 'distancia: %.2f'%math.sqrt(dist2 (a, b))
    S.clear()

    return ret
