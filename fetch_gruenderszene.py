import urllib2
import json
import re
import io
import string
from bs4 import BeautifulSoup
from startup_class import Startup

def loadUrl(url):
    #load url, clear scraped data from <br>
    response = urllib2.urlopen(url)
    newResponse = re.sub('<br />', ' ', response.read(), re.UNICODE)
    soup = BeautifulSoup(newResponse)

    #fetch initial startup data
    startupName = soup.find("div", "profile-additional-information").ul.li.text
    foundedIn = soup.find("div", "profile-additional-information").ul.li.findNextSibling("li").span.text
    startupDescription = soup.find("p", "teaser").findNextSibling("p").text

    #initiate startup object
    myStartup = Startup(startupName, startupDescription, foundedIn)

    #startup teaser
    startupTeaser = soup.find("p", "teaser").text
    myStartup.addTeaser(startupTeaser)

    #contact information
    try:
        contactList = soup.find("div", "contact-data").ul.findAll("li")
        i = 0
        for contItem in contactList:
            if i==0:
                contPhone = contItem.p.next_sibling.text
                myStartup.addPhone(contPhone)

            elif i==1:
                contEmail = contItem.p.next_sibling.text
                myStartup.addEmail(contEmail)

            elif i==2:
                contAddress = contItem.p.next_sibling.text
                myStartup.addAddress(contAddress)

            i += 1
    except:
        myStartup.addPhone("NN")
        myStartup.addEmail("NN")
        myStartup.addAddress("NN")

    #Startup Webprofile
    try:
        webList = soup.find("div", "webprofiles").ul.findAll("li")
    
        for webItem in webList:
            webUrl = webItem.p.a.get('href')
            webName = webItem.p.a.text
            myStartup.addUrl(webName, webUrl)
    except:
        myStartup.addUrl("NN","NN")

    #add founders
    try:
        founderList = soup.findAll("div", "head-information")

        for founder in founderList:
            founderName = founder.a.text
            founderUrl = founder.a.get('href')
            founderRole = founder.a.findNextSibling('p').text
            myStartup.addFounder(founderName, founderRole, founderUrl)
    except:
        myStartup.addFounder("NN", "NN", "NN")


    #add finance data
    try:
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
    except:
        myStartup.addFinance("NN", "NN", "NN")

    #add investor data
    try:
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
    except:
        myStartup.addInvestor("NN", "NN", "NN")

    #output data
    output = json.dumps(myStartup.getStartupData(), ensure_ascii=False)
    del myStartup
    return output


def loadUrlList(url):
    urlListOutput = []

    #load url, clear scraped data from <br>
    response = urllib2.urlopen(url)
    newResponse = re.sub('<br />', ' ', response.read())
    soup = BeautifulSoup(newResponse)

    #fetch initial startup data
    startupList = soup.find("ul", "single-letter-list").findAll("li")

    for startupItem in startupList:
        urlListOutput.append(
                startupItem.h3.a.get("href")
            )

    return urlListOutput


def loadDatabase(baseUrl, outputFile):
    with io.open(outputFile, 'a', encoding='utf-8') as f:
        f.write(unicode("{\"Startups\":["))
        i = 0
        #z = len(string.lowercase)

        for i in range(6,len(string.lowercase)):
            startupList = loadUrlList(baseUrl + string.lowercase[i]) #add letter [a-z] to url, according to its position in alphabet
            j = 1

            for startupItem in startupList:
                print startupItem
                f.write(unicode(loadUrl(startupItem)))
                if j < len(startupList):
                    f.write(unicode(",\n"))

                j += 1

        f.write(unicode("], \"DataSource\":\""+baseUrl+"\"}"))

    return "finished"


print loadDatabase('http://www.gruenderszene.de/datenbank/unternehmen/found/', "output.json")
