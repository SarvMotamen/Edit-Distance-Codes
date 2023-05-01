import numpy as np
import os
import random
from statistics import mean

def find_ops(opr, len_st, len_ed):
  i = len_st
  j = len_ed
  ins = dels = subs = 0
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
  return ins, dels, subs

MAX_N = 10

w_del = 1
w_in = 1
w_sub = 1
w_dup = 1/2
w_ded = 1/2

t = 0
ans = open("ans3.txt", "w")
test = open("gup_dist.txt", "r")
file_name = test.readline()[:-1]
while os.path.isfile(file_name):
#for po in range(0, 10):
  ans.write(file_name + "\n")
  rand = open("rand/" + file_name[6:], "r")
  st = rand.readline()[:-1]
  for i in range(0, MAX_N+1):
    ed = rand.readline()[:-1]

    ####################################   DYNAMIC ###########################################
    dists = np.matrix(np.ones((len(st)+1,len(ed)+1)) * np.inf)
    dist_org = np.matrix(np.ones((len(st)+1,len(ed)+1)) * np.inf)
    opr = np.matrix(np.zeros((len(st)+1,len(ed)+1)))
    # 0: no op / 1: in / 2: del / 3: sub

    ################# INITIALIZATION ##########################
    dists[0, 0] = 0
    dist_org[0, 0] = 0

    opr[0, 0] = 0

    if len(ed) != 0:
      for i in range(1, len(st)+1):
        dist_org[i, 0] = dist_org[i-1, 0] + w_del
        opr[i, 0] = 2
        if st[i-1] == st[i-2]:
          dists[i, 0] = dists[i-1, 0] + w_ded
        else:
          dists[i, 0] = dists[i-1, 0] + w_del

    if len(st) != 0:
      for j in range(1, len(ed)+1):
        dist_org[0, j] = dist_org[0, j-1] + w_in
        opr[0, j] = 1
        if ed[j-1] == ed[j-2]:
          dists[0, j] = dists[0, j-1] + w_dup
        else:
          dists[0, j] = dists[0, j-1] + w_in
        
    ################# UPDATE   ########################
    for i in range(1, len(st)+1):
      for j in range(1, len(ed)+1):
        d = [] # list of distances from which we will choose the minimum
        d_org = []
        ops = []
        stt = st[0:i]
        edd = ed[0:j]

        # insertion / duplication
        d_org.append(dist_org[i, j-1] + w_in)
        ops.append(1)
        if len(edd) > 1 and edd[-1] == edd[-2]: d.append(dists[i, j-1] + w_dup)
        else: d.append(dists[i, j-1] + w_in)

        # deletion / deduplication
        d_org.append(dist_org[i-1, j] + w_del)
        ops.append(2)
        if len(stt) > 1 and stt[-1] == stt[-2]: d.append(dists[i-1, j] + w_ded)
        else: d.append(dists[i-1, j] + w_del)

        # substitution
        if stt[-1] == edd[-1]: 
          d.append(dists[i-1, j-1])
          ops.append(0)
          d_org.append(dist_org[i-1, j-1])
        else: 
          d.append(dists[i-1, j-1] + w_sub)
          ops.append(3)
          d_org.append(dist_org[i-1, j-1] + w_sub)

        # update dists[i][j]
        dists[i, j] = min(d)
        dist_org[i, j] = min(d_org)
        opr[i, j] = ops[d_org.index(min(d_org))]
          
    #ins, dels, subs = find_ops(opr, len(st), len(ed))
    #t += 1
    #print(t)
    ans.write(str(dists[len(st),len(ed)]) + "\n" + str(dist_org[len(st),len(ed)]) + "\n") 
    #ans.write(", " + str(ins) + ", " + str(dels) + ", " + str(subs) + "\n")
  rand.close()
  t += 1
  print(t)
  test.readline()
  test.readline()
  test.readline()
  test.readline()
  test.readline()
  file_name = test.readline()[:-1]
  ans.flush()

test.close()
ans.close()
print("!")
