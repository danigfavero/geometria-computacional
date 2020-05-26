#!/usr/bin/env python
"""Algoritmo forca-bruta"""

from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
import math
from random import shuffle


def square_id(p, delta, off):
	plc = math.sqrt(delta)
	return (math.floor((2*(p.x + off))/plc), math.floor((2*(p.y+off))/plc))


def Prob (l):
	"Algoritmo probabilistico para encontrar o par de pontos mais proximo"

	if len (l) < 2: return None
	shuffle(l)
	
	offset = float("inf")

	for p in l:
		offset = min(offset, p.x, p.y)
	
	offset = min(0, offset)
	

	delt = dist2(l[0], l[1])
	S = {}
	S[square_id(l[0], delt, offset)] = 0
	S[square_id(l[1], delt, offset)] = 1
	a = l[0]
	b = l[1]
	control.freeze_update ()
	hia = a.hilight()
	hib = b.hilight()
	id = a.lineto (b)
	control.thaw_update() 
	control.update ()

	for i in range (2, len(l)):
		cur_id = square_id(l[i], delt, offset)
		updt = False
		for u in range(-2, 3):
			for v in range(-2, 3):
				nxt = (cur_id[0] + u, cur_id[1] + v)
				if nxt in S:
					dist = dist2(l[S[nxt]], l[i])
					if(dist < delt):
						delt = dist
						updt = True
						control.freeze_update ()
						if a != None: a.unhilight (hia)
						if b != None: b.unhilight (hib)
						if id != None: control.plot_delete (id)

						a = l[i]
						b = l[S[nxt]]

						hia = a.hilight ()
						hib = b.hilight ()
						id = a.lineto (b)
						control.thaw_update() 
						control.update ()
		if delt == 0:
			break
		if updt:
			S.clear()
			for j in range(0, i + 1):
				S[square_id(l[j], delt, offset)] = j
		else:
			S[cur_id] = i

	a.hilight('green')
	b.hilight('green')
	ret = Segment (a, b)
	ret.extra_info = 'distancia: %.2f'%math.sqrt (dist2 (a, b))
	S.clear()
	return ret
