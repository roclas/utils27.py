#!/usr/bin/env python

import os,sys,urllib2


filename=sys.argv[1]
fi=open(filename)

"""se trae la libreria Templater.py de github a local, se carga y se borra"""
response = urllib2.urlopen('https://raw.github.com/roclas/utils27.py/master/lib/Templater.py')
html = response.read()
#exec html
file=open("./Templater.py",'wa')
file.write(html)
file.close()
import Templater
for f in [ f for f in os.listdir(".") if f.startswith("Templater.py") ] : os.remove(f)


"""se carga el template"""
#template_file=os.path.abspath(__file__).split("/")[-1:][0].split(".")[:1][0]+".hql.tmpl"
template_file="training_sentiment_form.tmpl.html"
templater=Templater.Templater(template_file)

"""se crea el contexto"""
context={"lines":[x.decode("utf-8").strip() for x in fi.readlines()]}

"""se renderiza el template contextualizado"""
print templater.render(context).encode('ascii','ignore')




