import functools
import math

def is_within_polygon(polygon, point):
    A = []
    B = []
    C = []  
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        a = -(p2[1] - p1[1])
        b = p2[0] - p1[0]
        c = -(a * p1[0] + b * p1[1])

        A.append(a)
        B.append(b)
        C.append(c)

    D = []
    for i in range(len(A)):
        d = A[i] * point[0] + B[i] * point[1] + C[i]
        D.append(d)

    t1 = all(d >= 0 for d in D)
    t2 = all(d <= 0 for d in D)
    return t1 or t2

def convex_hull(points): 
    def cmp(a, b):
        return (a > b) - (a < b)

    def turn(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def left(hull, r):
        perimetro = 0
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != 1:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = functools.reduce(left, points, [])
    u = functools.reduce(left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l

def saint_john(large, L, small, S):
    hull = convex_hull(large)
    n = 0
    for s in small: 
        if is_within_polygon(hull, s):
            n += 1
    return n

def main():
    L = int(input())
    large = []
    for i in range(L):
        coord = input().split()
        x = int(coord[0])
        y = int(coord[1])
        large.append((x,y))
    S = int(input())
    small = []
    for i in range(S):
        coord = input().split()
        x = int(coord[0])
        y = int(coord[1])
        small.append((x,y))
    print(saint_john(large, L, small, S))

main()
