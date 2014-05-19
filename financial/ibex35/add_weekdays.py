#!/usr/bin/env python

import datetime,sys

inputfile=sys.argv[1]
weekdays=["mon","tue","wen","thu","fri","sat","sun"]

for l in open(inputfile).readlines():
	try:
		arr=l.split('"')
		date_str=arr[1]
		d,m,y=date_str.split("/")
		dt=datetime.date(int(y),int(m),int(d))
		weekday=weekdays[dt.timetuple()[6]]
		print "\"%s\",%s" %(weekday,l)
	except Exception as e:
		print "error: %s" %e




