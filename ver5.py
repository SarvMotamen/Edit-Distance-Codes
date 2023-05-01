import numpy as np
import os
import random
from statistics import mean

w_del = 1
w_in = 1
w_sub = 1
w_dup = 0.9
w_ded = 0.9

def find_ops(opr, len_st, len_ed):
    i = len_st
    j = len_ed
    ins = dels = subs = dups = deds = 0
    while i!=0 or j!=0:
        if opr[i, j] == 0:
            i -= 1
            j -= 1
        elif opr[i, j] == 1:
            j -= 1
            ins += 1
        elif opr[i, j] == 2:
            i -= 1
            dels += 1
        elif opr[i, j] == 3:
            i -= 1
            j -= 1
            subs += 1
        elif opr[i, j] == 4:
            j -= 1
            dups += 1
        elif opr[i, j] == 5:
            i -= 1
            deds += 1
      
    
    return ins, dels, subs, dups, deds

def findDist(st, ed):
    ####################################   DYNAMIC ###########################################
    dists = np.matrix(np.ones((len(st)+1,len(ed)+1)) * np.inf)
    opr = np.matrix(np.zeros((len(st)+1,len(ed)+1)))
    # 0: no op / 1: in / 2: del / 3: sub

    ################# INITIALIZATION ##########################
    dists[0, 0] = 0
    opr[0, 0] = 0
    
    if len(ed) != 0:
        for i in range(1, len(st)+1):
            if st[i-1] == st[i-2]: 
                dists[i, 0] = dists[i-1, 0] + w_ded
                opr[i,0] = 5
            else: 
                dists[i, 0] = dists[i-1, 0] + w_del
                opr[i,0] = 2

    if len(st) != 0:
        for j in range(1, len(ed)+1):
            if ed[j-1] == ed[j-2]: 
                dists[0, j] = dists[0, j-1] + w_dup
                opr[0,j] = 4
            else: 
                dists[0, j] = dists[0, j-1] + w_in
                opr[0,j] = 1
        
    ################# UPDATE   ########################
    for i in range(1, len(st)+1):
        for j in range(1, len(ed)+1):
            d = [] # list of distances from which we will choose the minimum
            ops = []
            stt = st[0:i]
            edd = ed[0:j]

            # insertion / duplication
            if len(edd) > 1 and edd[-1] == edd[-2]: 
                d.append(dists[i, j-1] + w_dup)
                ops.append(4)
            else: 
                d.append(dists[i, j-1] + w_in)
                ops.append(1)

            # deletion / deduplication
            if len(stt) > 1 and stt[-1] == stt[-2]: 
                d.append(dists[i-1, j] + w_ded)
                ops.append(5)
            else: 
                d.append(dists[i-1, j] + w_del)
                ops.append(2)

            # substitution
            if stt[-1] == edd[-1]: 
                d.append(dists[i-1, j-1])
                ops.append(0)
            else: 
                d.append(dists[i-1, j-1] + w_sub)
                ops.append(3)

            # update dists[i][j]
            dists[i, j] = min(d)
            opr[i, j] = ops[d.index(min(d))]
    if w_dup == 0.5 or w_dup == 0.51:
        final.write(str(opr) + " ")
    return find_ops(opr, len(st), len(ed))
   

file_name = "guppy/j58.txt"
final = open("for_58.txt", "w")
#



for w in range(1, 100):
    w_dup = w/100
    w_ded = w/100

    seq = open("rand1/" + file_name[6:], "r")
    st_read = seq.readline()[:-1]
    ed_read = seq.readline()[:-1]
    syn_read = seq.readline()[:-1]
    seq.close()

    ed_dist = findDist(st_read, ed_read)
    syn_dist = findDist(st_read, syn_read)
    
    

    print(w)
 
    final.write(str(w) + "\n" + str(ed_dist) + "\n" + str(syn_dist) + "\n")
final.close()
