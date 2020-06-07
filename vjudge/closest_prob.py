import math
import random

def dist2(a, b):
    return (b[0] - a[0])**2 + (b[1] - a[1])**2

def square_id(p, delta, offset):
    aux = math.sqrt(delta)
    return math.floor((2*(p[0] + offset))/aux), math.floor((2*(p[1]+offset))/aux)
       
def distancia(l, n):
    if n < 2:
        return None
    random.shuffle(l)
    
    offset = 100000000
    for p in l:
        offset = min(offset, p[0], p[1])
    offset = min(0, offset)
    
    delta = dist2(l[0], l[1])
    S = {}
    S[square_id(l[0], delta, offset)] = 0
    S[square_id(l[1], delta, offset)] = 1
    a = l[0]
    b = l[1]

    for i in range(2, n):
        current_id = square_id(l[i], delta, offset)
        update = False

        for u in range(-2, 3):
            for v in range(-2, 3):
                next = (current_id[0] + u, current_id[1] + v)
                if next in S:
                    dist = dist2(l[S[next]], l[i])
                    if dist < delta:
                        delta = dist
                        update = True
                        a = l[i]
                        b = l[S[next]]

        if delta == 0:
            break

        if update:
            S.clear()
            for j in range(0, i + 1):
                S[square_id(l[j], delta, offset)] = j
        else:
            S[current_id] = i

    return math.sqrt(dist2(a, b))

def main():
    n = int(input())
    while n != 0:
        pontos = []
        for i in range(n):
            coord = input().split()
            x = int(coord[0])
            y = int(coord[1])
            pontos.append((x,y))
        d = distancia(pontos, n)
        if d >= 10000:
            print("INFINITY")
        else:    
            print(d)
        n = int(input())

main()