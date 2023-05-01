import numpy as np
import os
import random
import statistics
from statistics import mean
import statsmodels.stats.power as smp
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.stats import norm

MAX_N = 10
inp = open("ans.txt", "r")
out = open("diff.txt", "w")

rand_diff = []
r_diff = []

file_name = inp.readline()[:-1]
#for po in range(0, 100):
while os.path.isfile(file_name):
  out.write(file_name + "\n")
  #print(po)
  with_d = float(inp.readline()[:-1])
  no_d = float(inp.readline()[:-1])
  dif = no_d - with_d
  out.write(str(dif) + "\n")

  d = []
  for i in range(0, MAX_N):
    with_d = float(inp.readline()[:-1])
    no_d = float(inp.readline()[:-1])
    d.append(no_d-with_d)
    r_diff.append(dif-(no_d-with_d))
  mean_dif = mean(d)
  rand_diff.append(dif-mean_dif)
  out.write(str(mean_dif) + "\n")
  file_name = inp.readline()[:-1]
'''  
print(mean(r_diff))
CI = st.t.interval(alpha=0.95, df=len(r_diff)-1, loc=np.mean(r_diff), scale=st.sem(r_diff)) 
print(CI)

power_analysis = smp.TTestIndPower()
power = power_analysis.power(effect_size = 0.2, alpha = 0.01, nobs1 = 1000, ratio = 1, alternative = 'two-sided')
print(power)
'''

sd = statistics.pstdev(rand_diff)
beta = norm.cdf(st.norm.ppf(1-0.005)+0.2/(sd/np.sqrt(1000))) - norm.cdf(-st.norm.ppf(1-0.005)+0.2/(sd/np.sqrt(1000)))
print(1-beta)

'''
plt.figure()
plt.hist(rand_diff, 20)
plt.figure()
plt.hist(r_diff, 20)
plt.show()
'''

inp.close()
out.close()
