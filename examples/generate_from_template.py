import os,sys,urllib2

"""se trae la libreria Templater.py de github a local, se carga y se borra"""
response = urllib2.urlopen('https://raw.github.com/roclas/utils27.py/master/Templater.py')
html = response.read()
#exec html
file=open("Templater.py",'wa')
file.write(html)
file.close()
import Templater
for f in [ f for f in os.listdir(".") if f.startswith("Templater.py") ] : os.remove(f)


"""se carga el template"""
#template_file=os.path.abspath(__file__).split("/")[-1:][0].split(".")[:1][0]+".hql.tmpl"
template_file=sys.argv[1]+".tmpl"
templater=Templater.Templater(template_file)

"""se crea el contexto"""
#properties_file=os.path.abspath(__file__).split("/")[-1:][0].split(".")[:1][0]+".properties.py"
properties_file=sys.argv[1]+".properties.py"
exec(open(properties_file))
#print(context)

"""se renderiza el template contextualizado"""
print templater.render(context)



