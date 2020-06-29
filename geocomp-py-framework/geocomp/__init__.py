# -*- coding: utf-8 -*-

"""Algoritmos de Geometria Computacional

Sub-modulos:
- closest: algoritmos para encontar o par de pontos mais próximo
- lineintersections: algoritmos para encontrar todas as intersecções de segmentos

- common:     classes e operacoes usadas por diversos algoritmos
- gui:        implementacoes das operacoes graficas
"""

from . import closest
from . import lineintersections
from . import triangulation
from . import convexhull
from .common.guicontrol import init_display
from .common.guicontrol import plot_input
from .common.guicontrol import run_algorithm
from .common.prim import get_count
from .common.prim import reset_count

children = (   ( 'triangulation',  None, 'Triangulação de Polígonos [EP1]' ),
               ( 'lineintersections',  None, 'Interseção de Todos os Segmentos [EP2]' ),
               ( 'closest',  None, 'Par Mais Próximo [EP3]' ),
               ( 'convexhull',  None, 'Fecho Convexo [EP4]' )
	)

__all__ = [p[0] for p in children]
