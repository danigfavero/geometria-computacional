def tuple_subtraction(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def signed_area_parallelogram(a, b, c):
    return cross(tuple_subtraction(b, a), tuple_subtraction(c, b))

def clockwise(a, b, c):
    return signed_area_parallelogram(a, b, c) < 0

def counter_clockwise(a, b, c):
    return signed_area_parallelogram(a, b, c) > 0

def windy_path(obstacles, n, directions):
    aux = [i + 1 for i in range(n)]

    init = 0
    for i in range(n):
        a = obstacles[i]
        b = obstacles[init]
        if a < b:
            init = i
    obstacles[0], obstacles[init] = obstacles[init], obstacles[0]
    aux[0], aux[init] = aux[init], aux[0]

    for i in range(n - 2):
        choice = i + 1
        for j in range(i + 2, n):
            if directions[i] == 'L':
                if clockwise(obstacles[i], obstacles[choice], obstacles[j]):
                    choice = j
            else:
                if counter_clockwise(obstacles[i], obstacles[choice], obstacles[j]):
                    choice = j
        obstacles[i + 1], obstacles[choice] = obstacles[choice], obstacles[i + 1]
        aux[i + 1], aux[choice] = aux[choice], aux[i + 1]

    for i in aux:
        print(i, end=' ')
    print('')

def main():
    n = int(input()) # 2 < n < 51
    obstacles = []
    for i in range(n):
        coord = input().split()
        x = int(coord[0])
        y = int(coord[1])
        obstacles.append((x,y))
    directions = list(input())
    windy_path(obstacles, n, directions)

main()