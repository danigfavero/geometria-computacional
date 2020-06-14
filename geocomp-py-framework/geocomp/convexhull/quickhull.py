#!/usr/bin/env python
"""Computa o fecho convexo 2D de uma coleção de n pontos, usando uma técnica
de divisão e conquista similar ao Quicksort."""

from geocomp.common.point import Point
from geocomp.common.polygon import Polygon
from geocomp.common import control
from geocomp.common.guiprim import *

def partition(P, p, r):
    pass

def quickhull_rec(P, p, r):
    pass

def Quickhull(P):
    '''Recebe uma coleção de pontos P e devolve seu fecho convexo'''
    n = len(P)
    if n == 1:
        hull = [P[0]]
    return hull