from geocomp.common import prim
from geocomp.common import point
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from bintrees import RBTree

def left(a, b, c):
    '''Verifica se o ponto c está à esquerda ou sobre a reta dada por ab'''
    area2 = (a.x * b.y + a.y * c.x + b.x * c.y - b.y * c.x - c.y * a.x - b.x * a.y)
    return area2 >= 0

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

def find_intersections(l, n):
    ''' Detecta e processa os pontos eventos da linha de varredura de modo a
    encontrar todas as intersecções.
    '''
    Q = sorted_extremes(l, n)
    T = RBTree()
    while not Q.is_empty():
        p = Q.pop_min()
        treat_event(p, Q, T)

def sorted_extremes(l, n):
    ''' Ordena os extremos dos n segmentos da lista l
    '''
    Q = RBTree()
    for s in l:
        if s.upper == s.lower:
            pass # TODO corner case!!!
        Q[s.upper] = Event("left", s)
        Q[s.lower] = Event("right", s)
    return Q

def treat_event(p, Q, T):
    ''' Recebe o ponto evento e o trata conforme seu tipo: extremo esquerdo,
    extremo direito e ponto de intersecção. 
    '''
    event = p[1]
    point = p[0]

    chave = 0 # TODO

    if event.t == "left":
        s = event.s
        T[chave] = s # TODO 
        try:
            pred = T.prev_item(chave)
            if s.intersects(pred):
                verify_new_event(p, Q, s, pred)
        except KeyError:
            pass
        try:
            succ = T.succ_item(chave)
            if s.intersects(succ):
                verify_new_event(p, Q, s, succ)
        except KeyError:
            pass

    if event.t == "right":
        s = event.s
        try:
            pred = T.prev_item(point)
            succ = T.succ_item(point)
            T.pop(chave) # TODO
            if pred.intersects(succ):
                verify_new_event(p, Q, succ, pred)
        except KeyError:
            T.pop(chave) # TODO

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
    if are_parallel(s1, s2):
        # A intersecção é um conjunto infinito de pontos
        # Vamos retornar só um deles
        if s1.lower.x >= s2.lower.x and s1.lower.x >= s2.upper.x:
            return s1.lower
        return s2.lower

    # A intersecção é de apenas um ponto
    s1_equation = line_equation(s1.upper, s1.lower)
    s2_equation = line_equation(s2.upper, s2.lower)
    zn = det(s1_equation[0], s1_equation[1], s2_equation[0], s2_equation[1])
    x = -det(s1_equation[2], s1_equation[1], s2_equation[2], s2_equation[1]) / zn
    y = -det(s1_equation[0], s1_equation[2], s2_equation[0], s2_equation[2]) / zn
    inter = point.Point(x,y)
    return inter


def line_equation(p, q):
    a = p.y - q.y
    b = q.x - p.x
    c = - a * p.x - b * p.y
    return a, b, c

def det(a, b, c, d):
    return a * d - b * c

def are_parallel(s1, s2):
    s1_slope = (s1.upper.y - s1.lower.y) / (s1.upper.x - s1.lower.x)
    s2_slope = (s2.upper.y - s2.lower.y) / (s2.upper.x - s2.lower.x)
    return s1_slope == s2_slope