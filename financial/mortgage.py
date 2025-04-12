#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

tae=0.045
years=30
times_per_year=12
payment_amount=4000
debt=600000
originaldebt=debt
total=0

cp=0
capitalpaid=[]
totalpaid=[]

interest=tae/times_per_year

#for y in range(years):
n=0;y=1;p=0
while(debt>0):
        for p in range(times_per_year):
                if(debt<0):break
                total+=payment_amount
                p=(p%times_per_year)+1
                old_debt=debt
                debt=debt*(1+interest)-payment_amount
                cp+=(old_debt-debt)
                totalpaid.append(total)
                capitalpaid.append(cp)
                print "year %s\tperiod %s\tdebt %s\tpaid %s(total=%s)\t%s(capital)\t%s(interest)" % (y,p,debt,payment_amount,total,old_debt-debt,payment_amount-(old_debt-debt))
                n+=1
        y+=1                       

plt.scatter(range(n),capitalpaid,color='blue')
plt.scatter(range(n),totalpaid,color='red')
plt.title("TotalPaid(red)=%s vs CapitalPaid(blue)=%s" %(total,cp))
plt.show()
plt.clf()
