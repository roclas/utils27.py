#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#############################
###WARNING###################
#############################
###NEEDS A CONTRACTS.TXT#####
###LIST TO KNOW REAL DATES###
###FROM WHICH TO START THE###
###ACCRUAL AND SETTLEMENT####
###PROCESS###################
#############################
###THE PRODUCTS LIST#########
###NEEDS TO BE SORTED########
###BY DATE###################
#############################
#############################

import sys,random,time,datetime,os


contracts=[]
##maybe reading one by one could be more efficient
current_time=time.mktime(datetime.datetime(1900, 1, 1).timetuple())
accrual_time=current_time
increment_time=24*60*60
with os.popen("head -n 200000 borrar_contracts.txt") as f:
    for line in f:
	if("account" in line): 
		#print line
		c=line.strip().split("\t")
		current_time=int(c[4])
		print accrual_time,current_time
		while(current_time>accrual_time):
			accrual_time+=increment_time
			for contract in contracts:
				print "accruing %s" %contract
		contracts.append((c[1]),)
		
