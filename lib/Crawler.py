import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

class Crawler:
	def __init__(self, root):
    		self.finalList = set()
		self.http = httplib2.Http()
		self.root= root

	def getAllUniqueLinks(self, link, spaces):
		if not (link.startswith("http")): 
				link=self.root+"/"+link
		result=[]
		try: status, response = self.http.request(link)
		except:
			print spaces+"cannot crowl into %s" % link
			return result
            	print spaces+link            
		for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    			if link.has_key('href'): 
				newlink=link['href']
				if not (newlink.startswith("http")): 
					if (newlink.startswith("/")): 
						newlink=self.getroot(link)+"/"+newlink
					else:	newlink=self.getdir(link)+"/"+newlink
				result.append(newlink)
		return result

	def getdir(self, link):
		try:parts=link.split("/")	
		except: return self.root
		if(parts[0].startswith("http")):
			return "/".join(parts[0:-1])
		else: return self.root

	def getroot(self, link):
		try:parts=link.split("/")	
		except: return self.root
		if(parts[0].startswith("http")):
			return "/".join(parts[0:2])
		else: return self.root
		
		
	def crawlSite(self, linksList,depth,maxdepth,spaces):
		if(depth==maxdepth):return
    		for link in linksList:
        		if link not in self.finalList:
            			self.finalList.add(link)
            			childLinks = self.getAllUniqueLinks(link,spaces)
            			length = len(childLinks)
            			print spaces+'Total links for this page: ' + str(length)
            			self.crawlSite(childLinks,depth+1,maxdepth,spaces+"  ")

if __name__ == '__main__': 
	crawler=Crawler("http://www.mlcsoluciones.com")
	crawler.crawlSite(["http://www.mlcsoluciones.com"],0,10," ")
