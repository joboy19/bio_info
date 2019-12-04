import numpy as np 
from quad_space import dynprog
import random as r
import time as t
import matplotlib.pyplot as plt

#find perfect matches of length k
#extended matches via greedy
#do banded dp within the band with best results
#for banded dp
#going to put code up for how hes going to test the code:
# - running time "easy" to assess - will add a generous cut-off for "how far past linear time"
# - heuristic: find top 10 diags, cluster them based on deviation*1.5, do banded dp on best cluster


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
    
    range_check = int(round(np.std(list(diag_scores.keys())) * 0.75))

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
            


def nicePrint(mat, a, b):
    out = [[(1, '_') for x in range(b+1)] for x in range(a+1)]
    for x in range(b+1):
        for y in range(a+1):
            if (x,y) in mat.keys():
                out[y][x] = mat[(x,y)]
    for x in out:
        print(x)
                       

#a = dynprogBanded("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBAACA", "CBACCCBA", 2, 2)
#a = dynprogBanded("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], 
#"AAAAACCDDCCDDAAAAACC", "CCAAADDAAAACCAAADDCCAAAA", 0, 1000)

#a = dynprogBanded("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBA", "CBACC", 3, 3)





def mainEverything(a, b, c, d):
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

#a = dynprogBanded("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBAACA", "CBACCCBA", 3, 3)
#a = mainEverything("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBAACA", "CBACCCBA")
#c = dynprogBanded("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],
#"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")


def test():
    vals = "ABCD"
    timesA = []
    timesB = []
    valsV = [x*10 for x in range(10, 100)]
    for x in valsV:
        string1 = "".join(r.choice(vals) for x in range(x))
        string2 = "".join(r.choice(vals) for x in range(x))
        time1 = t.time()
        a = dynprog("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], string1, string2)
        timesA.append(t.time()-time1)
        print(a[0])
        time1 = t.time()
        a = mainEverything("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], string1, string2)
        timesB.append(t.time()-time1)
        print(a[0])

    plt.plot(valsV, timesA)
    plt.plot(valsV, timesB)
    plt.show()



#b = mainEverything("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AAA", "AAA")