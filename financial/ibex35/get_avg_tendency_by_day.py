#!/usr/bin/env python

import sys

inputfile=sys.argv[1]

totals=[]
counter=0
up=True
for l in open(inputfile).readlines():
	try:
		arr=l.split('",')
		number=arr[4].replace('"',"").replace('%','').replace(",",'.')
		increase=float(number)
		if(bool(increase>0) == bool(up)):counter+=1
		else:
			totals.append(("up" if up else "down",counter))
			counter=1
			up=(increase>0)
	except:
		print "error in %s" % number
		pass


totals=[(x,y) for (x,y) in totals if y>0]
positive=[(x,y) for (x,y) in totals if x=="up"]
negative=[(x,y) for (x,y) in totals if x=="down"]

negative_avg=reduce(lambda t,(x,y):y+t, negative,0)/(1.0+len(negative))
positive_avg=reduce(lambda t,(x,y):y+t, positive,0)/(1.0+len(positive))

print "duracion media de tendencia positiva=%s dias" % positive_avg
print "duracion media de tendencia negativa=%s dias" % negative_avg
