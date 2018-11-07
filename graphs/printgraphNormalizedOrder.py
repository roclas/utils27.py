#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

d = {}
with open("standings.txt") as f:
    for line in f:
        (key, val) = line.split(",")
        d[key] = [int(x) for x in val.strip().split()]


users=d.keys()
weeks=range(len(d[users[0]]))

lines={}
for u in users:
    lines[u]=[0.0]
    for w in weeks:lines[u].append((int(d[u][w])+lines[u][-1]))

t=[x for x in np.array([ lines[u][1:] for u in users]).transpose()]
positions=[ reduce(lambda(ac,c,m),(n,b):
            (ac+[( c+1 if(n>m)or(c==0) else c ,b)], c+1, n)
            ,p,([],0,0)  )[0] for p in [sorted(zip(w,users)) for w in t]]
        
norm=dict([(u,[]) for u in users])
for(i,u)in [e for p in positions for e in p]: norm[u].append(i)

    
plt.ylabel("position"); plt.xlabel("week")
plt.yticks(color="w")
for u in users:plt.plot(weeks,[norm[u][w] for w in weeks],label=u)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),  shadow=True, ncol=8)
plt.show()
