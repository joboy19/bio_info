import numpy as np

#### question 1
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

#### question 2
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

def dynproglin(a, b, c, d):
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
    return first[0], outB, outA

###question 3
def scoreE(a, b, c, d):
    return b[a.index(c)][a.index(d)]

def scoreSeed(a, b, c):
    return sum([scoreE(a, b, x, x) for x in c])

def seedGetter(a, b, kmer):
    index_dict = []
    found = 0
    for x in range(len(a)-kmer):
        index_dict.append([a[x:x+kmer], []])
    for x in range(len(b)-kmer):
        for y in enumerate(index_dict):
            if b[x:x+kmer] == y[1][0]:
                found += 1
                y[1][1].append(x)
    return index_dict, (found>=1)

def findDiag(a, b, index_dict):
    diag_scores = {}
    for x in enumerate(index_dict):
        for y in x[1][1]:
            if (x[0] - y) in diag_scores:
                diag_scores[x[0] - y] = diag_scores[x[0] - y] + 1
            else:
                diag_scores[x[0] - y] = 1
    diag_scores = dict(sorted(diag_scores.items(), key=lambda kv: kv[1])[::-1][:10])

    #scoreSeed(a, b, x[1][0])
    
    range_check = int(round(np.std(list(diag_scores.keys())) * 1.5))

    diags = list(diag_scores.keys())

    clusters = {}
    
    for x in diags:
        clusters[x] = [x]
        for y in diags:
            if x - range_check <= y <= x + range_check:
                clusters[x] = clusters[x] + [y]
        
    cluster_scores = {}
    for x in clusters:
        cluster_score = 0
        for y in clusters[x]:
            cluster_score += diag_scores[x]
        cluster_scores[x] = cluster_score
    
    out_val = max(cluster_scores, key=cluster_scores.get)


    return out_val, range_check

def dynprogBanded(a, b, in_c, in_d, diag, k):
    print("-- running banded dp --")
    print("input lengths:", len(in_c), len(in_d))
    print("diag:", diag)
    print("k:", k)
    c = in_c
    d = in_d
    len1 = len(c)
    len2 = len(d)

    def score(x, y):
        if x == "-":
            return b[a.index(y)][-1]
        if y == "-":
            return b[a.index(x)][-1]
        return b[a.index(y)][a.index(x)]


    mat = {}

    if diag == 0:
        start_x = 0
        start_y = 0
    elif diag > 0:
        start_x = diag
        start_y = 0
    else:
        c, d = d, c
        len1, len2 = len2, len1
        diag = -1*diag
        start_x = diag
        start_y = 0

    x, y = start_x, start_y

    

    while (x < len1 + k + 1) and (y < len2 + 1):
        j = y
        
        #first i value of jth row: (cant check left, and checking
        #   if its out-of-bounds
        if (x-k) < 0:
            pass
        elif (x-k) == 0:
            mat[(x-k, j)] = (0, "E")
        elif j == 0:
            mat[(x-k, j)] = (0, "E")
        else:
            diags = mat[(x-k-1, j-1)][0] + score(d[j-1], c[x-k-1])
            ups = mat[(x-k,j-1)][0] + score("-",  d[j-1])
            if max([diags, ups, 0]) == diags:
                mat[(x-k, j)] = (diags, "D")
            elif max([diags, ups, 0]) == ups:
                mat[(x-k, j)] = (ups, "U")
            elif max([diags, ups, 0]) == 0: 
                mat[(x-k, j)] = (0, "E")

        #rest of i values on this row (can check all around),
        # (apart from the final value in row)
        for i in range(x-k+1, x+k):
            #check in bounds on left side
            if i < 0:
                pass
            elif i == 0:
                mat[(i, j)] = (0, "E")
            #check in bounds on right side
            elif i > len1:
                break
            #check if on first line
            elif j == 0:
                mat[(i, j)] = (0, "E")
            #else we can dynamic program
            else:
                diags = mat[(i-1, j-1)][0] + score(d[j-1], c[i-1])
                ups = mat[(i,j-1)][0] + score("-",  d[j-1])
                lefts = mat[(i-1,j)][0] + score("-",  c[i-1])

                if max([diags, ups, lefts, 0]) == diags:
                    mat[(i, j)] = (diags, "D")
                if max([diags, ups, lefts, 0]) == ups:
                    mat[(i, j)] = (ups, "U")
                if max([diags, ups, lefts, 0]) == lefts:
                    mat[(i, j)] = (lefts, "L")
                if max([diags, ups, lefts, 0]) == 0:
                    mat[(i, j)] = (0, "E")
            
                    
        #final value on row (i = x + k)
        #if out-of-bounds
        if x + k > len1:
            pass
        #else on first row
        elif j == 0:
            mat[(x+k, j)] = (0, "E")
        #else can check diag and left
        else:
            diags = mat[(x+k-1, j-1)][0] + score(d[j-1], c[x+k-1])
            lefts = mat[(x+k-1,j)][0] + score("-",  c[x+k-1])
            if max([diags, lefts, 0]) == diags:
                mat[(x+k, j)] = (diags, "D")
            elif max([diags, lefts, 0]) == lefts:
                mat[(x+k, j)] = (lefts, "U")
            elif max([diags, lefts, 0]) == 0: 
                mat[(x+k, j)] = (0, "E")
        x += 1
        y += 1
                      
    best_val = 0 
    for x in mat.keys():
        if mat[x][0] > best_val:
            best_val = mat[x][0]
            best_pos = x
    print("best val and best pos:", best_val, best_pos)

    crdX, crdY = best_pos[0], best_pos[1]
    next_val = best_val
    outa = []
    outb = []
    while next_val != 0:
        if mat[(crdX, crdY)][1] == "D":
            outa.append(crdX-1)
            outb.append(crdY-1)
            next_val = mat[(crdX-1, crdY-1)][0]
            crdX -= 1
            crdY -= 1
            
        if mat[(crdX, crdY)][1] == "L":
            next_val = mat[(crdX-1, crdY-1)][0]
            crdX -= 1
        
        if mat[(crdX, crdY)][1] == "U":
            next_val = mat[(crdX-1, crdY-1)][0]
            crdY -= 1
    

    if diag < 0:
        outa, outb = outb, outa

   
            
    #for line in mat: print(line)
    
    return (best_val, outa[::-1], outb[::-1])
            
def heuralign(a, b, c, d):
    kmer = 4
    while kmer > 0:
        index_dict, enough = seedGetter(c, d, kmer)
        if enough:
            break
        kmer -= 1
    diag, k = findDiag(a, b, index_dict)
    k = max(k, 1)
    a = dynprogBanded(a, b, c, d, diag, k)
    return a

c = dynprog("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")
d = dynproglin("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")
e = heuralign("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")







