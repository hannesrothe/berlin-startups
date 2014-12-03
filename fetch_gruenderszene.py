import urllib2
import json
from BeautifulSoup import BeautifulSoup
from startup_class import Startup

response = urllib2.urlopen('http://www.gruenderszene.de/datenbank/unternehmen/a-space-for-art')
soup = BeautifulSoup(response)

#print my_table
name = soup.find("h1", "profile-name").text
teaser = soup.find("p", "teaser").text
description = soup.find("p", "teaser").findNextSibling("p").text

mystartup = Startup(name, description, 2008)
mystartup.addTeaser(teaser)
       
print json.dumps(mystartup.getStartupData(), sort_keys = True)