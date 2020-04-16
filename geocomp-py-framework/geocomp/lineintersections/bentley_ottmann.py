from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from bintrees import AVLTree

class Event:
    "Ponto evento da linha de varredura"
    def __init__(self, t, *args):
        self.t = t
        if type == "left" or type == "right":
            self.s = list(args)[0]
        if type == "inter":
            self.s1 = list(args)[0]
            self.s2 = list(args)[1]


def Bentley_Ottmann(l):
    ''' Recebe uma coleção de segmentos e devolve o número de interseções
    presente na coleção
    '''
    
    find_intersections(l, len(l))

def sorted_extremes(l, n):
    ''' Ordena os extremos dos n segmentos da lista l
    '''
    Q = AVLTree()
    for s in l:
        if s.upper == s.lower:
            pass # TODO corner case!!!
        Q[s.upper] = Event("left", s)
        Q[s.lower] = Event("right", s)
    return Q

def find_intersections(l, n):
    ''' Detecta e processa os pontos eventos da linha de varredura de modo a
    encontrar todas as intersecções.
    '''
    Q = sorted_extremes(l, n)
    T = AVLTree()
    while not Q.is_empty():
        p = Q.pop_min()
        treat_event(p, Q, T)

def treat_event(p, Q, T):
    ''' Recebe o ponto evento e o trata conforme seu tipo: extremo esquerdo,
    extremo direito e ponto de intersecção. 
    '''
    event = p[1]
    point = p[0]

    if event.t == "left":
        s = event.s
        # T.insert(s) TODO oxe mas é uma symboltable, Qual é a key?
        # não esquece de passar essa chave pra "point" ou renomeie isso
        # usaremos essa chave pra achar o intersects
        try:
            pred = T.prev_item(point)
            if s.intersects(pred):
                verify_new_event(p, Q, s, pred)
        except KeyError:
            pass
        try:
            succ = T.succ_item(point)
            if s.intersects(succ):
                verify_new_event(p, Q, s, succ)
        except KeyError:
            pass

    if event.t == "right":
        s = event.s
        try:
            pred = T.prev_item(point)
            succ = T.succ_item(point)
            if pred.intersects(succ):
                verify_new_event(p, Q, succ, pred)
        except KeyError:
            pass

    if event.t == "inter":
        s1 = event.s1
        s2 = event.s2
        try:
            pred = T.pred_item(s1)
        except KeyError:
            pred = None
        try:
            succ = T.succ_item(s2)
        except KeyError:
            succ = None
        T.pop(s1)
        T.pop(s2)
        # T.insert(s2)
        # T.insert(s1)
        # na ordem inversa TODO
        if pred != None and pred.intersects(s2):
            verify_new_event(p, Q, pred, s2)
        if succ != None and s1.intersects(succ):
            verify_new_event(p, Q, s1, succ)

def verify_new_event(p, Q, s1, s2):
    ''' Verifica novo evento e registra intersecção
    '''
    q = intersection_point(s1, s2)
    if q > p and q not in Q:
        Q[q] = Event("inter", s1, s2)
        print(q)

def intersection_point(s1, s2):
    ''' Devolve um ponto no qual dois segmentos se intersectam
    '''
    # TODO como eu sei qual é o (primeiro) ponto no qual eles se intersectam
    pass
