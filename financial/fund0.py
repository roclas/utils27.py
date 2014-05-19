#!/usr/bin/env python

interest=0.08
taxes=0.25
years=40
anual_input=3600

commissions=[(0.02174*(27*anual_input)/(12.0*4)) for x in range(4*12)]+[0 for x in range((years-4)*12)]
commissions=[x+5 for x in commissions]
discounts_percentages=[(x%2)*0.01 for x in range(years)]

payed=0
amount=0
for y in range(years*12):
		if((y%12)==0):
			amount+=anual_input
			payed+=anual_input
			won=(amount-payed) if (amount-payed>0) else 0
		amount-=commissions[y]
		if((y%12)==0):
			print "year %s  amount %s  final amount %s"%(y/12+1,amount,amount-(won*(taxes)))
			if(y>11):
				amount*=(1+interest)
		if((y%12)==11):amount*=(1+discounts_percentages[y/12])
