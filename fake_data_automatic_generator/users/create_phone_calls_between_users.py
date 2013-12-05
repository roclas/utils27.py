#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


#argv1=number of calls
#argv1=number of diferent users

import sys,random,time,datetime

mytime=1386085884
for i in range(int(sys.argv[1])):
  user1=random.randint(0,int(sys.argv[2]))
  user2=random.randint(0,int(sys.argv[2]))
  if(user1==user2):continue
  mytime-=random.randint(0,140)
  date=datetime.datetime.fromtimestamp(mytime).strftime('%Y-%m-%d %H:%M:%S')
  duration=random.randint(0,1200)
  print "%d %d %d %s" %(user1,user2,duration,date)


