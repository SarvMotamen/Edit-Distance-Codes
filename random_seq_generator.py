import numpy as np
import os
import random
from statistics import mean

w_del = 1
w_in = 1
w_sub = 1
w_dup = 1/2
w_ded = 1/2

def find_ops(opr, len_st, len_ed):
  i = len_st
  j = len_ed
  ins_ = dels_ = subs_ = 0
  while i!=0 or j!=0:
    if opr[i, j] == 0:
      i -= 1
      j -= 1
    elif opr[i, j] == 1:
      j -= 1
      ins_ += 1
    elif opr[i, j] == 2:
      i -= 1
      dels_ += 1
    elif opr[i, j] == 3:
      i -= 1
      j -= 1
      subs_ += 1
  return ins_, dels_, subs_
  
def findDist(st, ed):
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
          
    ins_ed, dels_ed, subs_ed = find_ops(opr, len(st), len(ed))
    return ins_ed, dels_ed, subs_ed, ins_ed+dels_ed+subs_ed, dists[len(st),len(ed)]
  
def eqDist(st, ed, ins_org, dels_org, subs_org, n_org):
    ins_new, dels_new, subs_new, n_new, dist_new = findDist(st, ed)
    '''print("ins: ", ins_org, ins_new, "\n")
    print("dels: ", dels_org, dels_new, "\n")
    print("subs: ", subs_org, subs_new, "\n")
    print("n: ", n_org, n_new, "\n\n")'''
    if ins_new==ins_org and dels_new==dels_org and subs_new==subs_org and n_new==n_org:
        return dist_new
    else:
        return 0
        

    

MAX_N = 10

f = open("gup_dist.txt", "r")
defect = open("defect2.txt", "w")
final = open("final_result.txt", "w")
file_name = f.readline()[:-1]
t = 0
defect_n = 0
greater = 0
smaller = 0
equall = 0


  
while os.path.isfile(file_name):
#for op in range(0, 5):
  final.write(file_name+"\n")
  
  gup = open(file_name, "r")
  gup.readline()
  st_read = gup.readline()[:-1]
  gup.readline()
  ed_read = gup.readline()[:-1]
  gup.close

  ans = open("rand1/" + file_name[6:], "w")

  dup_dist = float(f.readline()[:-1])
  final.write(str(dup_dist) + "\n")
  f.readline()
  ins = int(f.readline()[:-1])
  dels = int(f.readline()[:-1])
  subs = int(f.readline()[:-1])
  n = ins + dels + subs
  
  ops = []
  for i in range(0, ins):
    ops.append(1)
  for i in range(0, dels):
    ops.append(2)
  for i in range(0, subs):
    ops.append(3) 

  ans.write(st_read + "\n")
  ans.write(ed_read + "\n")
  k = 0
  num = 0
  
  while k == 0 and num <= 200:
    st = st_read    
    random.shuffle(ops)
    
    x = random.sample(range(0, len(st)), n)
    x.sort(reverse=True)
    
    for i in range(0, n):
      if ops[i] == 1: 
        charr = random.sample(["A", "C", "G", "T"], 1)[0]
        #print(charr)
        st = st[0:x[i]+1] + charr + st[x[i]+1:]
      elif ops[i] == 2: 
        st = st[0:x[i]] + st[x[i]+1:]
      elif ops[i] == 3: 
        charr = random.sample(["A", "C", "G", "T"], 1)[0]
        while charr == st[x[i]]:
          charr = random.sample(["A", "C", "G", "T"], 1)[0]
        #print(st[x[i]], charr)
        st = st[0:x[i]] + charr + st[x[i]+1:]
        
    k = eqDist(st_read, st, ins, dels, subs, n)
    #print("len:", len(st), len(ed_read), "\n")
    if k != 0: 
      ans.write(st + "\n")
      final.write(str(k) + "\n")
      if k > dup_dist: greater += 1
      elif k < dup_dist: smaller += 1
      else: equall += 1
      
      #print("!", st, "\n")
    #else: print(st, "\n")
    num += 1
    if num == 200: 
        defect.write(file_name + "\n")
        defect_n += 1;
        print("defected:")
  ans.close()
  t += 1
  print(t)
  file_name = f.readline()[:-1]
print("number of defefcted: ", defect_n)
final.write("\n" + str(greater) + "\n" + str(smaller) + "\n" + str(equall) + "\n")



'''while os.path.isfile(file_name):
#for op in range(0, 5):
  gup = open(file_name, "r")
  gup.readline()
  stt = gup.readline()[:-1]
  gup.readline()
  ed = gup.readline()[:-1]
  gup.close

  ans = open("rand/" + file_name[6:], "w")

  f.readline()
  f.readline()
  ins = int(f.readline()[:-1])
  dels = int(f.readline()[:-1])
  subs = int(f.readline()[:-1])
  n = ins + dels + subs

  ans.write(stt + "\n")
  ans.write(ed + "\n")
  for k in range(0, MAX_N):
    st = stt
    # deletions
    x_del = random.sample(range(0, len(st)), dels)
    x_del.sort()
    for i in range(0, dels):
      st = st[0:x_del[i]] + "e" + st[x_del[i]+1:]

    # substitutions
    al = range(0, len(st))
    s = set(x_del)
    x_new = [k for k in al if k not in s]
    x_sub = random.sample(x_new, subs)
    for i in range(0, subs):
      charr = random.sample(["A", "C", "G", "T"], 1)[0]
      while charr == st[x_sub[i]]:
        charr = random.sample(["A", "C", "G", "T"], 1)[0]
      st = st[0:x_sub[i]] + charr + st[x_sub[i]+1:]
    
    #insertions
    x_noin = []
    for t in x_del: 
      if t!=0: x_noin.append(t-1)
      x_noin.append(t)
    x_noin = list(set(x_noin))
    x_noin.sort()
    al = range(0, len(st))
    s = set(x_noin)
    x_new = [k for k in al if k not in s]
    x_ins = random.sample(x_new, ins)
    x_ins.sort(reverse=True)
    for i in range(0, ins):
      charr = random.sample(["A", "C", "G", "T"], 1)[0]
      st = st[0:x_ins[i]+1] + charr + st[x_ins[i]+1:]

    # delete e
    lst = st.split("e")
    st = "".join(lst)
    ans.write(st + "\n")
  ans.close()
  file_name = f.readline()[:-1]'''
