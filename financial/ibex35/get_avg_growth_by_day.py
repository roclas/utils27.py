#!/usr/bin/env python

import sys

inputfile=sys.argv[1]

totals={}
counts={}
for l in open(inputfile).readlines():
	try:
		arr=l.split('",')
		weekday=arr[0].replace('"',"")
		avg=arr[4].replace('"',"").replace(',',".")[:-1]
		if(not totals.has_key(weekday)):
			totals[weekday]=float(avg)
			counts[weekday]=1
		else:
			totals[weekday]+=float(avg)
			counts[weekday]+=1
	except Exception as e:
		print "error: %s" %e


for k in ["mon","tue","wen","thu","fri","sat","sun"]:
#for k in totals.keys():
	print "on %s: %s (%s / %s)" %(k,totals[k]/counts[k],totals[k],counts[k])
	




