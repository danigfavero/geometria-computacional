def esquerda(x, y, z):
    return (y[0] - x[0]) * (z[1] - x[1]) - (z[0] - x[0]) * (y[1] - x[1])

def pertence(poligono, ponto):
    wn = 0 
    poligono = tuple(poligono[:]) + (poligono[0],)

    for i in range(len(poligono)-1):    
        if poligono[i][1] <= ponto[1]:       
            if poligono[i+1][1] > ponto[1]:   
                if esquerda(poligono[i], poligono[i+1], ponto) > 0:
                    wn += 1 
        else:
            if poligono[i+1][1] <= ponto[1]:
                if esquerda(poligono[i], poligono[i+1], ponto) < 0:
                    wn -= 1           
    return wn != 0

def main():
    n = int(input())
    while n != 0:
        poligono = []
        for i in range(n):
            coord = input().split()
            x = int(coord[0])
            y = int(coord[1])
            poligono.append((x,y))
        coord = input().split()
        x = int(coord[0])
        y = int(coord[1])
        if pertence(poligono, (x,y)):
            print("T")
        else:    
            print("F")
        n = int(input())

main()