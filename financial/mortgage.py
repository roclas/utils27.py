#!/usr/bin/env python

tae=0.032
years=35
times_per_year=12
payment_amount=1200
debt=350000
total=0


interest=tae/times_per_year

#for y in range(years):
y=1;p=0
while(debt>0):
        for p in range(times_per_year):
                if(debt<0):break
                total+=payment_amount
                p=(p%times_per_year)+1
                old_debt=debt
                debt=debt*(1+interest)-payment_amount
                print "year %s\tperiod %s\tdebt %s\tpaid %s(total=%s)\t%s(capital)\t%s(interest)" % (y,p,debt,payment_amount,total,old_debt-debt,payment_amount-(old_debt-debt))
        y+=1                       
