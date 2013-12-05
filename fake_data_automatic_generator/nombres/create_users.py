#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys,random,sha,unicodedata
def remove_accents(s): 
	return s.translate(None,"áéíóúñÁÉÍÓÚÑ").lower()

hombres=[x.strip() for x in open("final_hombres.txt").readlines()]
mujeres=[x.strip() for x in open("final_mujeres.txt").readlines()]
apellidos=[x.strip() for x in open("final_apellidos.txt").readlines()]
prefijos=[601, 602, 603, 604, 611, 612, 613, 614, 621, 623, 624, 631, 632, 640, 641, 642, 643, 644, 668, 672, 673, 674, 681, 682, 683, 684, 694, 698]


for i in range(int(sys.argv[1])):
	sexo= "M" if random.random()>=0.5 else "F" 
	if(sexo):n=hombres[random.randint(0,len(hombres)-1)]
	else:n=mujeres[random.randint(0,len(mujeres)-1)]
	a1=apellidos[random.randint(0,len(apellidos)-1)]
	a2=apellidos[random.randint(0,len(apellidos)-1)]
	email=remove_accents(n[:3]+a1[:4])+"@"+sha.sha(str(i)+n+a1+a2).hexdigest()[:5]+".com"
	movil=prefijos[random.randint(0,len(prefijos)-1)]*1000000+random.randint(0,999999)
	print "%d	%s	%s	%s	%s	%d	%s" %(i,sexo,n,a1,a2,movil,email)


