#!/usr/bin/env python
import BaseHTTPServer,os,sys,cgi,urllib2

filename=sys.argv[1]


def apply_template(filename):
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
	context={"lines":[x.decode("utf-8").strip() for x in fi.readlines()[-5:]]}
	fi.close()

	"""se renderiza el template contextualizado"""
	return templater.render(context).encode('ascii','ignore')

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        print self.path
        #self.path = '/simplehttpwebpage_content.html'
	filepath="/".join(os.path.realpath(__file__).split("/")[:-1])+'/'+self.path
        self.send_response(200)
	if self.path.endswith(".css"):
		self.send_header('Content-type', 'text/css')
        self.end_headers()
	if(not os.path.isfile(filepath)):
        	self.wfile.write(apply_template(filename))
	else: 
		f = open(filepath)
        	self.wfile.write(f.read())
        	f.close()
        return 
    def do_POST(self):
	ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    	if ctype == 'multipart/form-data':
        	postvars = cgi.parse_multipart(self.rfile, pdict)
    	elif ctype == 'application/x-www-form-urlencoded':
        	length = int(self.headers.getheader('content-length'))
        	postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
    	else:
        	postvars = {}
        #print "POST "+self.path 
	for i in postvars:
	  try:
		if(i[0]=='l'):
			os.system("echo %s %s >> logs.txt" %(postvars["t"+i[1:]][0],postvars[i][0]))
	  except:
		pass
		#print sys.exc_info()[0]
	return self.do_GET()

server_class = BaseHTTPServer.HTTPServer
httpd = server_class(("localhost", 9000), MyRequestHandler)

httpd.serve_forever()
