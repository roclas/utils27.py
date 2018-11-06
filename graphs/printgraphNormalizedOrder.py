#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

d = {}
with open("standings.txt") as f:
    for line in f:
        (key, val) = line.split(",")
        d[key] = val.strip().split()

users=d.keys()
weeks=range(len(d[users[0]]))

lines={}
for u in users:
    lines[u]=[0.0]
    for w in weeks:lines[u].append((int(d[u][w])+lines[u][-1]))

maxs=[max(x) for x in np.array([ lines[u][1:] for u in users]).transpose()]
t=[x for x in np.array([ lines[u][1:] for u in users]).transpose()]
positions=[sorted(zip(w,users)) for w in t]
for p in positions:
    m=min(x[0] for x in p);c=0
    for i in range(len(p)):
        (v,u)=p[i];c+=1
        if(v>m)or(i==0):p[i]=(c,u)
        else:
            p[i]=(p[i-1][0],u);m=v
        

norm={}
for u in users: norm[u]=[]
for p in positions:
    for (i,u) in p: norm[u].append(i)
    

plt.ylabel("position"); plt.xlabel("week")
plt.yticks(color="w")
for u in users:plt.plot(weeks,[norm[u][w] for w in weeks],label=u)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),  shadow=True, ncol=8)
plt.show()
    
