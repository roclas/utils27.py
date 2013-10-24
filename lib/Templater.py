import sys
from django.template import Template, Context
from django.conf import settings
settings.configure()

class Templater:
	def __init__(self,templatefile=None):
		if(templatefile): self.loadTemplate(templatefile)

	def loadTemplateText(self, templatetext):
		self.t = Template(templatetext)
		
	def loadTemplate(self, templatefilename,fromFile=True):
		if (not fromFile):return self.loadTemplateText(templatefilename)
		try: 
			fp=open(templatefilename)
			self.t = Template(fp.read())
			fp.close()
		except Exception: 
			sys.stderr.write( "couldn't load %s file\nusing %s as template\n" % (templatefilename,templatefilename))
			return self.loadTemplateText(templatefilename)

	def render(self,context):
		return self.t.render(Context(context))

if __name__ == '__main__': 
	templater=Templater(".test_template.tmpl")
	print templater.render({"one":"uno","two":2.0})
