#!/usr/bin/env python

tae=0.07
taxes=0.21
years=40
anual_amount=3600

interest=tae

amount=0
for y in range(years):
	amount+=anual_amount
	amount*=1+interest
	print "year %s   amount %s   final %s" % (y+1,amount,amount-amount*interest*taxes)
	
