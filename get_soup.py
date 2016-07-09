import urllib2
from bs4 import BeautifulSoup
class SoupGet(object):
    
    def soupget(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response)
        return soup