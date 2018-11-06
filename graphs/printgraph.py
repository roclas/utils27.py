#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

d = {}
with open("standings.txt") as f:
    for line in f:
        (key, val) = line.split(",")
        d[key] = val.strip().split()

weeks=range(len(d[d.keys()[0]]))

lines={}
for u in d.keys():
    lines[u]=[0.0]
    for w in weeks:lines[u].append((int(d[u][w])+lines[u][-1]))

maxs=[max(x) for x in np.array([ lines[u][1:] for u in d.keys()]).transpose()]

plt.ylabel("position"); plt.xlabel("week")
plt.yticks(color="w")
for u in d.keys():plt.plot(weeks,[lines[u][1:][w]/maxs[w] for w in weeks],label=u)
plt.legend()
plt.show()
    
