#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#argv1=number of calls
#argv1=number of diferent users

import sys,random,time,datetime,os

percentage_inner_calls=0.15
number_clients=int(sys.argv[2])-1
number_inner_calls=int(percentage_inner_calls*int(sys.argv[1]))
start_id=random.randint(0,number_clients)
end_id=random.randint(0,number_clients)
internal_phones=[]
prefijos=[601, 602, 603, 604, 611, 612, 613, 614, 621, 623, 624, 631, 632, 640, 641, 642, 643, 644, 668, 672, 673, 674, 681, 682, 683, 684, 694, 698]

if(end_id<start_id):
	internal_phones+=[x.strip().split("\t")[5] for x in os.popen("sed -n '%d,%dp' < users.txt" % (1,end_id)).readlines()]
	start_id=end_id
	end_id=number_clients

internal_phones+=[x.strip().split("\t")[5] for x in os.popen("sed -n '%d,%dp' < users.txt" % (start_id,end_id)).readlines()]
print len(internal_phones)

mytime=1386085884
for i in range(int(sys.argv[1])):
  user1=random.randint(0,int(number_clients))
  prob=random.random()
  if(prob>percentage_inner_calls):destination=prefijos[random.randint(0,len(prefijos)-1)]*1000000+random.randint(0,999999)
  else:destination=int(internal_phones[random.randint(0,len(internal_phones)-1)])
  mytime-=random.randint(0,140)
  date=datetime.datetime.fromtimestamp(mytime).strftime('%Y-%m-%d %H:%M:%S')
  duration=random.randint(0,1200)
  print "%d %d %d %s" %(user1,destination,duration,date)
