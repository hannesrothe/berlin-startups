import urllib2
import json
import re
from BeautifulSoup import BeautifulSoup
from startup_class import Startup

#load url, clear scraped data from <br>
response = urllib2.urlopen('http://www.gruenderszene.de/datenbank/unternehmen/a-space-for-art')
newResponse = re.sub('<br />', ' ', response.read())
soup = BeautifulSoup(newResponse)

#fetch initial startup data
startupName = soup.find("div", "profile-additional-information").ul.li.text
foundedIn = soup.find("div", "profile-additional-information").ul.li.findNextSibling("li").span.text
startupDescription = soup.find("p", "teaser").findNextSibling("p").text

#initiate startup object
myStartup = Startup(startupName, startupDescription, foundedIn)

#additional startup information
startupTeaser = soup.find("p", "teaser").text
myStartup.addTeaser(startupTeaser)

#add founders
founderList = soup.findAll("div", "head-information")

for founder in founderList:
    founderName = founder.a.text
    founderUrl = founder.a.get('href')
    founderRole = founder.a.findNextSibling('p').text
    myStartup.addFounder(founderName, founderRole, founderUrl)


#output data
print json.dumps(myStartup.getStartupData(), sort_keys = True)