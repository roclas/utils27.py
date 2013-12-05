#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#argv1=number of contracts
#argv2=number of diferent users

import sys,random,time,datetime,os

products=[x.strip().split("\t") for x in open("products.txt").readlines()]

start_time=1323013884
mytime=start_time
minimum_posible_time=-2208985807
time_increment_signal=-1
time_interval=3600

id=0
for c in range(int(sys.argv[1])):
  user=random.randint(0,int(sys.argv[2]))
  product=products[random.randint(0,len(products)-1)]
  mytime+=(time_increment_signal)*random.randint(0,time_interval)
  if(mytime<minimum_posible_time):
	break
	#mytime+=time_interval
	#time_increment_signal=1
  #elif(mytime>start_time):
	#mytime-=time_interval
	#time_increment_signal=-1
  date=datetime.datetime.fromtimestamp(mytime).strftime('%Y-%m-%d %H:%M:%S')
  print "%s\t%s\t%s\t%s\t%s" %(id,user,product,date,mytime)
  id+=1
	
	
