import numpy as np
import os
import random
from statistics import mean

w_del = 1
w_in = 1
w_sub = 1
w_dup = 0.9
w_ded = 0.9
  
def findDist(st, ed):
    ####################################   DYNAMIC ###########################################
    dists = np.matrix(np.ones((len(st)+1,len(ed)+1)) * np.inf)
    # 0: no op / 1: in / 2: del / 3: sub

    ################# INITIALIZATION ##########################
    dists[0, 0] = 0
    
    if len(ed) != 0:
        for i in range(1, len(st)+1):
            if st[i-1] == st[i-2]: dists[i, 0] = dists[i-1, 0] + w_ded
            else: dists[i, 0] = dists[i-1, 0] + w_del

    if len(st) != 0:
        for j in range(1, len(ed)+1):
            if ed[j-1] == ed[j-2]: dists[0, j] = dists[0, j-1] + w_dup
            else: dists[0, j] = dists[0, j-1] + w_in
        
    ################# UPDATE   ########################
    for i in range(1, len(st)+1):
        for j in range(1, len(ed)+1):
            d = [] # list of distances from which we will choose the minimum
            stt = st[0:i]
            edd = ed[0:j]

            # insertion / duplication
            if len(edd) > 1 and edd[-1] == edd[-2]: d.append(dists[i, j-1] + w_dup)
            else: d.append(dists[i, j-1] + w_in)

            # deletion / deduplication
            if len(stt) > 1 and stt[-1] == stt[-2]: d.append(dists[i-1, j] + w_ded)
            else: d.append(dists[i-1, j] + w_del)

            # substitution
            if stt[-1] == edd[-1]: d.append(dists[i-1, j-1])
            else: d.append(dists[i-1, j-1] + w_sub)

            # update dists[i][j]
            dists[i, j] = min(d)
          
    return dists[len(st),len(ed)]
   
        
final = open("final_result_all.txt", "w")
#

for w in np.arange(0.01, 1, 0.01):
    w_dup = w
    w_ded = w
    t = 0
    
    names = open("names.txt", "r")
    file_name = names.readline()[:-1]
    
    greater = 0
    smaller = 0
    equall = 0

    while os.path.isfile(file_name):
    #for op in range(0, 5):
        #final.write(file_name+"\n")

        seq = open("rand1/" + file_name[6:], "r")
        st_read = seq.readline()[:-1]
        ed_read = seq.readline()[:-1]
        syn_read = seq.readline()[:-1]
        seq.close()

        ed_dist = round(findDist(st_read, ed_read), 2)
        #print(ed_dist)
        #final.write(str(ed_dist) + "\n")
        syn_dist = round(findDist(st_read, syn_read), 2)
        #print(syn_dist)
        #final.write(str(syn_dist) + "\n")
         
        
        if syn_dist > ed_dist: greater += 1
        elif syn_dist < ed_dist: smaller += 1
        else: equall += 1
          
        file_name = names.readline()[:-1]
        
        t+=1
        print(w, ": ", t)
    names.close() 
    final.write(str(w) + "\n" + str(greater) + "\n" + str(smaller) + "\n" + str(equall) + "\n")
final.close()
