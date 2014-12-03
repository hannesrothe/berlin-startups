import urllib2
import json
import re
import io
from bs4 import BeautifulSoup
from startup_class import Startup

def loadUrl(url):
    #load url, clear scraped data from <br>
    response = urllib2.urlopen(url)
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

    #add finance data
    financeList = soup.find("div", "company-finance").table.findAll("tr")
    i = 0
    for finItem in financeList:
        if i==0:
            finType = finItem.find("td","value").text
        elif i==1:
            finValue = finItem.find("td","value").text
        elif i==2:
            finDate = finItem.find("td","value").text
        i += 1
        
    myStartup.addFinance(finType, finValue, finDate)

    #add investor data
    investorList = soup.find(id="investor-view").ul.findAll("li")

    i=0
    for invItem in investorList:
        if i==0: #Managers
            j = 0
            invListMan = invItem.findAll("p")
            for invItemMan in invListMan:
                if j != 0:
                    invType = "Manager"
                    invName = re.sub('\(([]\<]?\d{1,3})\%\)','', invItemMan.text)

                    rgQuery = re.compile('\(([]\<]?\d{1,3})\%\)') #Search for String: (100%) or (<1%)
                    rgResult = re.search(rgQuery, invItemMan.text)
                    invShare = rgResult.group(1)
                    myStartup.addInvestor(invName, invType, invShare)
                j += 1
        elif i==1: #Supporters
            j = 0
            invListSup = invItem.findAll("p")
            for invItemSup in invListSup:
                if j != 0:
                    invType = "Investor and Supporter"
                    invName = re.sub('\(([]\<]?\d{1,3})\%\)','', invItemSup.text)

                    rgQuery = re.compile('\(([]\<]?\d{1,3})\%\)') #Search for String: (100%) or (<1%)
                    rgResult = re.search(rgQuery, invItemSup.text)
                    invShare = rgResult.group(1)
                    myStartup.addInvestor(invName, invType, invShare)
                j += 1
        i +=1

    #output data
    return json.dumps(myStartup.getStartupData(), sort_keys = True, ensure_ascii=False)


output = loadUrl('http://www.gruenderszene.de/datenbank/unternehmen/ohsaft');

with io.open('output.json', 'w', encoding='utf-8') as f:
  f.write(unicode(output))
  f.close()
if f.closed == True:
    print (output)