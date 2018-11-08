#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

################################################
####put all the data in a dictionary###
################################################
u= dict(
        [(a,[int(x) for x in b.strip().split()]) 
            for (a,b) in [l.split(",") 
                for l in open("standings.txt").readlines()]]
        )

l=dict([(e,reduce(lambda ac,x:ac+[int(x)+ac[-1]],u[e],[0])[1:]) for e in u])

################################################
####convert the points in possitions/rankings###
################################################
tr=[x for x in np.array([ l[e] for e in u]).transpose()]
rank=[ reduce(lambda(ac,c,m),(n,b):
            (ac+[( c+1 if(n>m)or(c==0) else c ,b)], c+1, n)
            ,p,([],0,0)  )[0] for p in [sorted(zip(t,u)) for t in tr]]

norm=dict([(e,[]) for e in u])
for(i,e)in [j for p in rank for j in p]: norm[e].append(i)
    
################################################
####print the graph###
################################################
plt.ylabel("position"); plt.xlabel("week")
plt.yticks(color="w")
w=range(len(u[u.keys()[0]]))
for e in u:plt.plot(w,[norm[e][t] for t in w],label=e)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),  shadow=True, ncol=8)
plt.show()
