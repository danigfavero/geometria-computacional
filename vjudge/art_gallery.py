def contains_critical_point(gallery, n):
    if (n < 4):
        return False

    sign = True
    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n
        dx1 = gallery[k][0] - gallery[j][0]
        dy1 = gallery[k][1] - gallery[j][1]
        dx2 = gallery[i][0] - gallery[j][0]
        dy2 = gallery[i][1] - gallery[j][1]
        zcrossproduct = dx1 * dy2 - dy1 * dx2

        if i == 0:
            sign = zcrossproduct > 0
        elif sign != (zcrossproduct > 0):
            return True
    return False

def main():
    n = int(input())
    while n != 0:
        gallery = []
        for i in range(n):
            coord = input().split()
            x = int(coord[0])
            y = int(coord[1])
            gallery.append((x,y))
        if contains_critical_point(gallery, n):
            print("Yes")
        else:    
            print("No")
        n = int(input())

main()