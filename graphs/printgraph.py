#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

d = {}
with open("standings.txt") as f:
    for line in f:
        (key, val) = line.split(",")
        d[key] = val.strip().split()

lines={}
for u in d.keys():
    lines[u]=[]
    total=0.0
    for w in range(len(d[d.keys()[0]])):
        total=int(d[u][w])+total
        lines[u].append(total/(w+1))



weeks=range(0,len(lines[d.keys()[0]]))
for u in d.keys():
    plt.plot(weeks,lines[u],label=u)
plt.legend()
plt.show()
    
