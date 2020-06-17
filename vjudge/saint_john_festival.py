import itertools

def is_inside(x1, y1, x2, y2, x3, y3, x, y): 
    side_1 = (x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)
    side_2 = (x - x3) * (y2 - y3) - (x2 - x3) * (y - y3)
    side_3 = (x - x1) * (y3 - y1) - (x3 - x1) * (y - y1)
    return (side_1 < 0.0) == (side_2 < 0.0) == (side_3 < 0.0)

def saint_john(large, L, small, S):
    n = 0
    for s in small:
        for t in itertools.combinations(large, 3):
            if is_inside(t[0][0], t[0][1], t[1][0], t[1][1], t[2][0], t[2][1], s[0], s[1]):
                n += 1
                break
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
