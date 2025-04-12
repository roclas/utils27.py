#!/usr/bin/env python

tae=0.25
taxes=0.00
years=8
times_per_year=12
amount=100000

interest=tae/times_per_year

for y in range(years):
	for p in range(times_per_year):
		print "year %s   period %s  amount %s" % (y,p,amount)
		amount=amount*(1+interest)-(amount*interest*taxes)
	
