from geocomp.common import prim
from geocomp.common import point
from geocomp.common import segment
from geocomp.common import control
from geocomp.common.prim import area2, left
from geocomp import config
from bintrees import RBTree
from .my_tree import MyTree
from sortedcontainers import SortedKeyList


dic = {}
intersections = []

class Event:
    "Ponto evento da linha de varredura"
    def __init__(self, t, *args):
        self.t = t
        if t == "left" or t == "right":
            self.s = list(args)[0]
        if t == "inter":
            self.s1 = list(args)[0]
            self.s2 = list(args)[1]
    def __str__(self):
        if self.t == "inter":
            s = "tipo: " + str(self.t) + " seg: " + str(self.s1) + str(self.s2)
        else:
            s = "tipo: " + str(self.t) + " seg: " + str(self.s)
        return s 

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
    T = SortedKeyList()
    while not Q.is_empty():
        p = Q.pop_min()
        treat_event(p, Q, T)

def sorted_extremes(l, n):
    ''' Ordena os extremos dos n segmentos da lista l
    '''
    Q = RBTree()
    for s in l:
        dic[s] = (s, s)
        if s.upper == s.lower:
            pass # TODO corner case!!!
        Q[s.lower] = Event("left", s)
        Q[s.upper] = Event("right", s)
    return Q

def treat_event(p, Q, T):
    ''' Recebe o ponto evento e o trata conforme seu tipo: extremo esquerdo,
    extremo direito e ponto de intersecção. 
    '''
    event = p[1]
    point = p[0]

    print(event, end="\n\n")
    print("ANTES")
    # print(dic)
    for seg in T:
        print("key: ", str(seg))
    
    linea = 0
    point.hilight("green")
    if event.t == "left":
        s = event.s
        T.add((s,s))
        linea = control.plot_vert_line(s.lower.x, "cyan")
        control.sleep() 
        control.update()
        try:
            prev_index = T.bisect_left((s, s))
            prev_index -= 1
            if prev_index >= 0:
                pred = T[prev_index][1]
                if s.intersects(pred):
                    verify_new_event(point, Q, s, pred)
        except IndexError:
            pass
        try:
            next_index = T.bisect_right(s)
            if next_index <= len(T):
                succ = T[next_index][1]
                if s.intersects(succ):
                    verify_new_event(point, Q, s, succ) 
        except IndexError:
            pass

    if event.t == "right":
        s = dic[event.s]
        segmnt = s[1]
        linea = control.plot_vert_line(segmnt.upper.x, "cyan")
        control.sleep()
        control.update()
        try:
            print(s)
            prev_index = T.bisect_left(s)
            next_index = T.bisect_right(s)
            prev_index -= 1
            if prev_index >= 0 and next_index <= len(T):
                pred = T[prev_index][1]
                succ = T[next_index][1]
                T.pop(T.index(s))    
                if pred.intersects(succ):
                    verify_new_event(point, Q, succ, pred)
        except IndexError:
            T.pop(T.index(s))

    if event.t == "inter":
        s1 = event.s1
        s2 = event.s2
        rs1 = dic[s1]
        rs2 = dic[s2]
        intersection = intersection_point(s1,s2)
        intersections.append(intersection)
        intersections[len(intersections) - 1].hilight("yellow")
        print(len(intersections))
        linea = control.plot_vert_line(intersection.x, "cyan")
        control.sleep()
        control.update()
        try:
            prev_index = T.bisect_left(rs1)
            prev_index -= 1
            if prev_index < 0:
                pred = None
            else:
                pred = T[prev_index][1]
        except IndexError:
            pred = None
        try:
            next_index = T.bisect_right(rs2)
            if next_index >= len(T):
                succ = None
            else:
                succ = T[next_index][1]
        except IndexError:
            succ = None
        print("s1: ", s1, " rs1: ", rs1)
        print("s2: ", s2, " rs2: ", rs2, "\n")
        T.pop(T.index(rs1))
        T.pop(T.index(rs2))
        # Insere ao contrário
        new_s1 = segment.Segment(intersection, s1.upper)
        new_s2 = segment.Segment(intersection, s2.upper)
        T.add((new_s2, s2))
        T.add((new_s1, s1))
        dic[s1] = (new_s1, s1)
        dic[s2] = (new_s2, s2)
        
        if pred != None and pred.intersects(s2):
            verify_new_event(point, Q, pred, s2, intersection)
        if succ != None and s1.intersects(succ):
            verify_new_event(point, Q, s1, succ, intersection)

    control.plot_delete(linea)
    control.sleep()
    control.update()
    point.unhilight()

    print("DEPOIS")
    for seg in T:
        print("key: ", str(seg))
    print("")
           
def verify_new_event(p, Q, s1, s2, inter=None):
    ''' Verifica novo evento e registra intersecção
    '''
    if inter == None:
        inter = intersection_point(s1, s2)
    q = inter
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