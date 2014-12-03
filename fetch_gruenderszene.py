import urllib2
import json
from BeautifulSoup import BeautifulSoup
from startup_class import Startup

response = urllib2.urlopen('http://www.gruenderszene.de/datenbank/unternehmen/a-space-for-art')
soup = BeautifulSoup(response)

#print my_table
startupName = soup.find("div", "profile-additional-information").ul.li.text
foundedIn = soup.find("div", "profile-additional-information").ul.li.findNextSibling("li").span.text
startupTeaser = soup.find("p", "teaser").text
startupDescription = soup.find("p", "teaser").findNextSibling("p").text
founderList = soup.findAll("div", "head-information")

for founder in founderList:
    founderName = founder.text
    print founderName



mystartup = Startup(startupName, startupDescription, foundedIn)
mystartup.addTeaser(startupTeaser)


       
print json.dumps(mystartup.getStartupData(), sort_keys = True)