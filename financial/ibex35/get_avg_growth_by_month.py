#!/usr/bin/env python

import sys

inputfile=sys.argv[1]

totals={}
counts={}
for l in open(inputfile).readlines():
	try:
		arr=l.split('",')
		month=arr[1].split("/")[1]
		avg=arr[4].replace('"',"").replace(',',".")[:-1]
		if(not totals.has_key(month)):
			totals[month]=float(avg)
			counts[month]=1
		else:
			totals[month]+=float(avg)
			counts[month]+=1
	except Exception as e:
		print "error: %s" %e


meses=["","enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
for k in totals.keys():
	i=int(k)
	print "en %s: %s por ciento de subida de media (%s / %s)" %(meses[i],totals[k]/counts[k],totals[k],counts[k])
	




