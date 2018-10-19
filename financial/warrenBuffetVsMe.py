#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

interestMe=0.05
interestWarren=0.2
taxesMe=0.0
taxesWarren=0.0
n_years=50
times_per_year=12
amountMe=3000
amountWarren=200000
years=range(datetime.datetime.now().year, datetime.datetime.now().year+n_years)


interestW=interestWarren/times_per_year
interestM=interestMe/times_per_year
warren=[]
me=[]

for y in years:
    for p in range(times_per_year):
        amountMe=amountMe*(1+interestM)-(amountMe*interestM*taxesMe)
        amountWarren=amountWarren*(1+interestW)-(amountWarren*interestW*taxesWarren)
    me.append(amountMe)
    warren.append(amountWarren)
    print "warren=%s, me=%s" % (amountWarren,amountMe)




plt.scatter(years,me,color='blue')
plt.scatter(years,warren,color='red')
plt.title("Warren(red)=%s vs Me(blue)=%s" %(amountWarren,amountMe))
plt.show()
plt.clf()
