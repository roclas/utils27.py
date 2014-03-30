#!/usr/bin/env python

tae=0.03
taxes=0.21
years=35
times_per_year=4
amount=1000

interest=tae/times_per_year

for y in range(years):
	for p in range(times_per_year):
		print "year %s   period %s  amount %s" % (y,p,amount)
		amount=amount*(1+interest)-(amount*interest*taxes)
	
