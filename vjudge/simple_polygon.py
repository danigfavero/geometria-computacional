""" Inspirado no código C++ em:
http://geomalgorithms.com/a09-_intersect-3.html#simple_Polygon()
"""
from bintrees import RBTree

def area2 (a, b, c):
    return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])

def left (a, b, c):
    return area2(a, b, c) > 0

class Segment:
    def __init__(self, lower, upper, i, j):
        self.lower = lower
        self.upper = upper
        self.i = i
        self.j = j

    def has_left(self, point):
        return left(self.init, self.to, point)

    def __lt__(self, other):
        if type(self) != type(other):
            return False
        if other.has_left(self.lower):
            return True
        return False

    def __le__(self, other):
        if type(self) != type(other):
            return False
        if other.has_left(self.lower) or (other.lower == self.self.lower and self.upper[1] < other.supper[1]):
            return True
        return False 

        def colinear_with(self, point):
            return area2(self.lower, self.upper, point) == 0

    def has_inside(self, point):
        if not self.colinear_with(point):
            return False
        if self.lower[0] != self.to[0]:
            return self.lower[0] <= point[0] <= self.upper[0] \
                   or self.upper[0] <= point[0] <= self.lower[0]
        else:
            return self.lower[1] <= point[1] <= self.upper[1] \
                   or self.upper[1] <= point[1] <= self.lower[1]

    def intersects_inside(self, other_segment) -> bool:
        if self.colinear_with(other_segment.lower)    \
           or self.colinear_with(other_segment.upper)   \
           or other_segment.colinear_with(self.lower) \
           or other_segment.colinear_with(self.upper):
            return False

        return (left(self.lower, self.upper, other_segment.lower)
                ^ left(self.lower, self.upper, other_segment.upper))            \
               and (left(other_segment.lower, other_segment.upper, self.lower)
                   ^ left(other_segment.lower, other_segment.upper, self.upper))

    def intersects(self, other_segment) -> bool:
        if self.intersects_inside(other_segment):
            return True

        return self.has_inside(other_segment.lower)    \
               or self.has_inside(other_segment.upper)   \
               or other_segment.has_inside(self.lower) \
               or other_segment.has_inside(self.upper)

class Event:
    def __init__(self, t, s):
        self.t = t
        self.s = s

def intersects_polygon(n, s1, s2):
    if (s1.j + 1) % n == s2.i or (s2.j + 1) % n == s1.i:
        return False
    return s1.intersects(s2)

def sorted_extremes(P, n):
    queue = RBTree()
    for i in range(n):
        j = (i+1) % n
        s = Segment(P[i], P[j], i, j)
        queue[P[i]] = Event("left", s)
        queue[P[j]] = Event("right", s)
    return queue

def is_simple(P, n):
    event_queue = sorted_extremes(P, n)
    sweep_line = RBTree()

    while not event_queue.is_empty():
        e = event_queue.pop_min()
        s = e.s

        if e.t == "left":
            sweep_line[s] = s
            try:
                pred = sweep_line.prev_key(s)
                if intersects_polygon(n, s, pred):
                    return False
            except KeyError:
                pass
            try:
                succ = sweep_line.succ_key(s)
                if intersects_polygon(n, s, succ):
                    return False
            except KeyError:
                pass

        else:
            try:
                pred = sweep_line.prev_key(s)
                succ = sweep_line.succ_key(s)
                sweep_line.pop(s)
                if intersects_polygon(n, pred, succ):
                    return False
            except KeyError:
                sweep_line.pop(s)
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