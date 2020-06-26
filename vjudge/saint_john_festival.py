import functools
import math


def left (a, b, c):
    return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0]) > 0

def area(a, b, c): 
    return abs((a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1])  + c[0] * (a[1] - b[1])) / 2.0) 

def is_inside_triangle(a, b, c, p): 
    A = area(a, b, c)  
    A1 = area(p, b, c)  
    A2 = area(a, p, c) 
    A3 = area(a, b, p) 

    return A == A1 + A2 + A3

def is_inside_polygon(polygon, point):
    n = len(polygon)
    if n == 3:
        return is_inside_triangle(polygon[0], polygon[1], polygon[2], point)
    if n == 4:
        return is_inside_triangle(polygon[0], polygon[1], polygon[2], point) or \
        is_inside_triangle(polygon[0], polygon[1], polygon[3], point)

    mid = n//2
    if left(polygon[0], polygon[mid], point):
        return is_inside_polygon(polygon[:mid], point)
    return is_inside_polygon(polygon[mid:], point)

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
    hull.sort()
    n = 0
    for s in small: 
        if is_inside_polygon(hull, s):
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
