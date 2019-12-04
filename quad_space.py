import numpy as np 

#todo - do the matrix on paper

def nicePrint(mat):
    for x in mat:
        print(x)

def dynprog(a, b, c, d):
    len1 = len(c)
    len2 = len(d)
    def score(x, y):
        if x == "-":
            return b[a.index(y)][-1]
        if y == "-":
            return b[a.index(x)][-1]
        return b[a.index(y)][a.index(x)]

    mat = []

    for x in range(len1+1):
        mat.append([])
        for y in range(len2+1):
            mat[x].append((0, "E"))
    
    #"L" means same array, -1 postion
    #"U" means same position, -1 array

    for x in range(1, len1+1):
        mat[x][0] = (max([mat[x - 1][0][0] + score("-", c[x-1]), 0]), "E")

    for y in range(1, len2+1):
        mat[0][y] = (max([mat[0][y-1][0] + score("-", d[y-1]), 0]), "E")
    
    for x in range(1, len1+1):
        for y in range(1, len2+1): #pointers for cell
            i = mat[x-1][y-1][0] + score(d[y-1], c[x-1])
            j = mat[x-1][y][0] + score("-",  c[x-1])
            k = mat[x][y-1][0] + score("-",  d[y-1])
            
            if max([i, j, k, 0]) == i:
                mat[x][y] = (i, "D")
            if max([i, j, k, 0]) == j:
                mat[x][y] = (j, "U")
            if max([i, j, k, 0]) == k:
                mat[x][y] = (k, "L")
            if max([i, j, k, 0]) == 0:
                mat[x][y] = (0, "E")
    
    #nicePrint(mat)
            
    bestVal = 0 
    for x in range(len1+1):
        for y in range(len2+1):
            if mat[x][y][0] > bestVal:
                bestVal = mat[x][y][0]
                crdX = x
                crdY = y
    nextVal = bestVal
    outa = []
    outb = []
    while nextVal != 0:
        if mat[crdX][crdY][1] == "D":
            outa.append(crdX-1)
            outb.append(crdY-1)
            nextVal = mat[crdX-1][crdY-1][0]
            crdX -= 1
            crdY -= 1

        if mat[crdX][crdY][1] == "U":
            nextVal = mat[crdX-1][crdY-1][0]
            crdX -= 1
        
        if mat[crdX][crdY][1] == "L":
            nextVal = mat[crdX-1][crdY-1][0]
            crdY -= 1
            
    #for line in mat: print(line)
    
    return bestVal, outa[::-1], outb[::-1]


#dynprog("ABC", [[1,-1,-2,-1], [-1,2,-4,-1], [-2,-4,3,-2], [-1,-1,-2,0]], "AB", "CA")

#dynprog("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "BBA", "BAC")

#print(dynprog("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD"))

"""
a = dynprog("ABCD",
    [[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], 
    "AAAA", 
    "CCAA")

a = dynprog("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBAACA", "CBACCCBA")
c = dynprog("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")
"""

def nicePrint(mat):
    for x in mat:
        print(x)
#print(c)