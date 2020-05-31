""" Inspirado no código C++ em:
http://geomalgorithms.com/a09-_intersect-3.html#simple_Polygon()
"""
from bintrees import RBTree

class Segment:
    pass

class Event:
    "Ponto evento da linha de varredura"
    def __init__(self, t, *args):
        self.t = t
        if t == "left" or t == "right":
            self.s = list(args)[0]
        if t == "inter":
            self.s1 = list(args)[0]
            self.s2 = list(args)[1]

def intersects(P, s1, s2):
    pass

def is_simple(P, n):
    event_queue = RBTree()
    sweep_line = RBTree()

    while not event_queue.is_empty():
        e = event_queue.pop_min()
        s = e.s

        if e.t == "left":
            sweep_line[e] = s
            try:
                pred = sweep_line.prev_item(e)[0]
                if intersects(P, s, pred):
                    return False
            except KeyError:
                pass
            try:
                succ = sweep_line.succ_item(e)[0]
                if intersects(P, s, succ):
                    return False
            except KeyError:
                pass

        else:
            try:
                pred = sweep_line.prev_item(e)[0]
                succ = sweep_line.succ_item(e)[0]
                sweep_line.pop(e)
                if intersects(P, pred, succ):
                    return False
            except KeyError:
                sweep_line.pop(e)
    return True

def main():
    n = int(input())
    while n != 0:
        P = []
        for i in range(n):
            coord = input().split()
            x = int(coord[0])
            y = int(coord[1])
            P.append((x,y))
        if is_simple(P, n):
            print("YES")
        else:    
            print("NO")
        n = int(input())

main()