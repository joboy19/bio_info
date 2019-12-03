import numpy as np 

#todo - do the matrix on paper

def nicePrint(mat):
    for x in mat:
        print(x)

def dynProgGlob(a, b, c, d):
    len1 = len(c)
    len2 = len(d)
    
    def score(x, y):
        if (x == "-") and (y == "-"):
            return b[-1][-1]
        if x == "-":
            return b[a.index(y)][-1]
        if y == "-":
            return b[-1][a.index(x)]
        return b[a.index(y)][a.index(x)]

    mat = []

    for x in range(len1+1):
        mat.append([])
        for y in range(len2+1):
            mat[x].append((0, "E"))
    
    #"L" means same array, -1 postion
    #"U" means same position, -1 array

    for x in range(1, len1+1):
        mat[x][0] = (max([mat[x - 1][0][0] + score("-", c[x-1])]), "U")

    for y in range(1, len2+1):
        mat[0][y] = (max([mat[0][y-1][0] + score("-", d[y-1])]), "L")
    
    for x in range(1, len1+1):
        for y in range(1, len2+1): #pointers for cell
            i = mat[x-1][y-1][0] + score(d[y-1], c[x-1])
            j = mat[x-1][y][0] + score("-",  c[x-1])
            k = mat[x][y-1][0] + score("-",  d[y-1])
            
            if max([i, j, k]) == i:
                mat[x][y] = (i, "D")
            if max([i, j, k]) == j:
                mat[x][y] = (j, "U")
            if max([i, j, k]) == k:
                mat[x][y] = (k, "L")
            
    outa = ""
    outb = ""
    crdX = len1
    crdY = len2
    #nicePrint(mat)

    while not ((crdX == 0) and (crdY == 0)):
        if mat[crdX][crdY][1] == "D":
            outa += c[crdX-1]
            outb += d[crdY-1]
            nextVal = mat[crdX-1][crdY-1][0]
            crdX -= 1
            crdY -= 1

        if mat[crdX][crdY][1] == "U":
            outa += c[crdX-1]
            outb += "-"
            nextVal = mat[crdX-1][crdY-1][0]
            crdX -= 1
        
        if mat[crdX][crdY][1] == "L":
            outa += "-"
            outb += d[crdY-1]
            nextVal = mat[crdX-1][crdY-1][0]
            crdY -= 1
            
    #for line in mat: print(line)
    
    return  (outa[::-1], outb[::-1])


def nws(a, b, c, d):
    def score(x, y):
        if (x == "-") and (y == "-"):
            return b[-1][-1]
        if x == "-":
            return b[a.index(y)][-1]
        if y == "-":
            return b[-1][a.index(x)]
        return b[a.index(y)][a.index(x)]
    
    scoreMat = [[],[]]
    
    for x in range(len(d)+1):
        scoreMat[0].append(0)
        scoreMat[1].append(0)

    for j in range(1, len(d) + 1):
        scoreMat[0][j] = scoreMat[0][j-1] + score(d[j-1], "-")
    
    for i in range(1, len(c) + 1):
        scoreMat[1][0] = scoreMat[0][0] + score(c[i-1], "-")
        for j in range(1, len(d) + 1):
            ssub = scoreMat[0][j-1] + score(c[i-1], d[j-1])
            ddel = scoreMat[0][j] + score(c[i-1], "-")
            iins = scoreMat[1][j-1] + score(d[j-1], "-")
            scoreMat[1][j] = max([ssub, ddel, iins])
        scoreMat[0] = list(scoreMat[1])
    lastline = []
    for j in range(len(d)+1):
        lastline.append(scoreMat[1][j])
    return lastline


def hir(a, b, c, d):
    z = ""
    w = ""
    if len(c) == 0:
        for j in range(len(d)):
            z += "-"
            w += d[j]
    elif len(d) == 0:
        for i in range(len(c)):
            z += c[i]
            w += "-" 
    elif len(c) == 1 or len(d) == 1:
        (z, w) = dynProgGlob(a, b, c, d)
    else:
        clen = len(c)
        cmid = int(len(c)/2)
        dlen = len(d)

        scoreL = nws(a, b, c[:cmid], d)
        scoreR = nws(a, b, c[cmid:clen][::-1], d[::-1])

        listt = [sum(x) for x in zip(scoreL, scoreR[::-1])]
        dmid = listt.index(max(listt))

        one = hir(a, b, c[0:cmid], d[0:dmid])
        two = hir(a, b, c[cmid:], d[dmid:])

        (z, w) = (one[0] + two[0]), (one[1] + two[1])

    
    return (z, w)

def startend(a, b, c, d):
    len1 = len(c)
    len2 = len(d)
    def score(x, y):
        if (x == "-") and (y == "-"):
            return b[-1][-1]
        if x == "-":
            return b[a.index(y)][-1]
        if y == "-":
            return b[-1][a.index(x)]
        return b[a.index(y)][a.index(x)]

    mat = [[],[]]

    for x in range(0, len1+1):
        mat[0].append("temp")
        mat[1].append("temp")
    
    #"L" means same array, -1 postion
    #"U" means same position, -1 array

    mat[0][0] = (0, 0, 0)
    bestVal = [0, 0, 0, 0, 0] #bestvals: value, positionx, posistiony, startx, starty


    for x in range(1, len1+1):
        next0 = max([mat[0][x-1][0] + score("-", c[x-1]), 0])
        if next0 == 0:
            mat[0][x] = (next0, x, 0)
        else:
            if next0 > bestVal[0]:
                bestVal = (next0, x, 0, mat[0][x-1][1], mat[0][x-1][2])
            mat[0][x] = (next0, 0, mat[0][x-1][2])
    

    
    for y in range(1, len2+1): #pointers for cell
        next0 = max([mat[0][0][1] + score("-", d[y-1]), 0])
        if next0 == 0:
            mat[1][0] = (0, 0, y)
        else:
            if next0 > bestVal[0]:
                bestVal = (next0, 0, y, mat[0][0][1], mat[0][0][2])

        for n in range(1, len1+1):  #y = current row being done, i is along the row
            i = mat[0][n-1][0] + score(d[y-1], c[n-1]) 
            j = mat[0][n][0] + score("-",  d[y-1])
            k = mat[1][n-1][0] + score(c[n-1],  "-")

            nextVal = max([i, j, k, 0])

            if nextVal > bestVal[0]:
                bestVal[0], bestVal[1], bestVal[2] = nextVal, y, n
                bestFound = True
            
            if nextVal == i:
                if bestFound:
                    bestVal[3], bestVal[4] = mat[0][n-1][1], mat[0][n-1][2]
                mat[1][n] = (i, mat[0][n-1][1], mat[0][n-1][2])
            if nextVal == j:
                if bestFound:
                    bestVal[3], bestVal[4] = mat[0][n][1], mat[0][n][2]
                mat[1][n] = (j, mat[0][n][1], mat[0][n][2])
            if nextVal == k:
                if bestFound:
                    bestVal[3], bestVal[4] = mat[1][n-1][1], mat[1][n-1][2]
                mat[1][n] = (k, mat[1][n-1][1], mat[1][n-1][2])
            if nextVal == 0:
                mat[1][n] = (0, n, y)
            
            bestFound = False
        
        mat[0] = list(mat[1])
            
    #for line in mat: print(line)
    
    return bestVal

def mainEverything(a, b, c, d):
    first = startend(a, b, c, d)
    seqA, seqB = False, False


    second = hir(a, b, d[first[4]:first[1]] ,  c[first[3]:first[2]])

    
    numA = first[4]
    numB = first[3]
    outA = []
    outB = []

    for x in range(len(second[0])):
        if second[0][x] == "-":
            numB += 1
            continue
        if second[1][x] == "-":
            numA += 1
            continue
        outA.append(numA)
        outB.append(numB)
        numA += 1
        numB += 1
    return first[0], outA, outB, second


a = mainEverything("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC", "CCAAADDAAAACCAAADDCCAAAA")
#b = mainEverything("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"AACAAADAAAACAADAADAAA", "CDCDDD")
#c = mainEverything("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")
#d = mainEverything("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "CBACCCBA", "AABBAACA")



print(a)
