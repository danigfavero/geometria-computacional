# -*- coding: utf-8 -*-
"""Algoritmos para o problema da triangulação de polígonosl.

Algoritmos disponveis:
- Remoção de orelhas
"""

from . import ear_clipping

children = [['ear_clipping', 'Ear_clipping', 'Remoção de orelhas']]

__all__ = [a[0] for a in children]