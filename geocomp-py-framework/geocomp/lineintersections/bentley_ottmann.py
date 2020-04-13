from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from bintrees import AVLTree

def Bentley_Ottmann(l):
    ''' Recebe uma coleção de segmentos e devolve o número de interseções
    presente na coleção
    '''
    
    find_intersections(l, len(l))

def sorted_extremes(l, n):
    ''' Ordena os extremos dos n segmentos da lista l
    '''
    q = AVLTree()
    for s in l:
        if s.upper == s.lower:
            pass # TODO corner case!!!
        q[s.upper] = s
        q[s.lower] = s
    return q

def find_intersections(l, n):
    q = sorted_extremes(l, n)
    t = AVLTree()
    while not q.is_empty():
        p = q.pop_min()
        treat_event(p, q, t)

def treat_event(p, q, t):
    s = p[1]
    e = p[0]

    if e == s.upper:
        # t.insert(s) TODO oxe mas é uma symboltable, qual é a key?
        # não esquece de passar essa chave pra "e" ou renomeie isso
        # usaremos essa chave pra achar o intersects
        try:
            pred = t.prev_item(e)
            if s.intersects(pred):
                verify_new_event(p, q, s, pred)
        except KeyError:
            pass
        try:
            succ = t.succ_item(e)
            if s.intersects(succ):
                verify_new_event(p, q, s, succ)
        except KeyError:
            pass

    if e == s.lower:
        try:
            pred = t.prev_item(e)
            succ = t.succ_item(e)
            if pred.intersects(succ):
                verify_new_event(p, q, succ, pred)
        except KeyError:
            pass

    if False: # TODO se p é ponto de intersecção
        pass

 

def verify_new_event(p, q, s, t):
    # TODO pensar em todo esse caso de pto de intersecção
    pass