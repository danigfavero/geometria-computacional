# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Fecho Convexo:

Dada uma coleção P de pontos do plano, determinar o fecho convexo de P.

Algoritmos disponveis:
- Quickhull
"""
from . import quickhull

children = [
	[ 'quickhull', 'Quickhull', 'Quickhull' ]
]

__all__ = [a[0] for a in children]
