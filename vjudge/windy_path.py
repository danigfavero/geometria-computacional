def windy_path(obstacles, n, directions):
    print(-1)

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