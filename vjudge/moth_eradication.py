from functools import reduce
from math import sqrt

def distancia(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def fecho_convexo(pontos): 
    def cmp(a, b):
        return (a > b) - (a < b)

    def vira(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def esquerda(fecho, r):
        perimetro = 0
        while len(fecho) > 1 and vira(fecho[-2], fecho[-1], r) != 1:
            fecho.pop()
        if not len(fecho) or fecho[-1] != r:
            fecho.append(r)
        return fecho

    pontos = sorted(pontos)
    l = reduce(esquerda, pontos, [])
    u = reduce(esquerda, reversed(pontos), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l


def main():
    n = int(input())
    contador = 1
    while n != 0:
        pontos = []
        for i in range(n):
            coord = input().split()
            x = float(coord[0])
            y = float(coord[1])
            pontos.append((x,y))
        
        print(f'Region #{contador}:')
        contador += 1
        fecho = fecho_convexo(pontos)
        print(f'({fecho[0][0]},{fecho[0][1]})', end='')
        for ponto in reversed(fecho):
            print(f'-({ponto[0]},{ponto[1]})', end='', sep='')
        print("")
        perimetro = 0
        m = len(fecho)
        for i in range(m):
            perimetro += distancia(fecho[i], fecho[(i+1)%m])
        print("Perimeter length = {:.2f}\n".format(perimetro))
        
        n = int(input())

main()