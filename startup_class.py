import re

class Startup(object):
	name = ""
	urlList = []

	def __init__(self, name, description, founding_year):
		self.name = ""
		self.description = ""
		self.teaser =""
		self.founding_year = 0
		self.founder = []
		self.finance = []
		self.investors = []
		self.address = ""
		self.phone = ""
		self.email = ""
		self.urlList = []

		self.name = name
		self.description = description
		self.founding_year = founding_year

	def addTeaser (self, teaser):
		self.teaser = teaser

	def addFounder (self, name, position, url):
		self.founder.append({
			"Name": name,
			"Position": position,
			"Url": url
			})

	def addFinance (self, finType, finValue, date):
		self.finance.append({
			"Type": finType,
			"Company Value": finValue,
			"Data collected on": date
			})

	def addInvestor (self, invName, invType, invShare):
		self.investors.append({
			"Name": invName,
			"Type": invType,
			"Shares": invShare
			})

	def addAddress(self, address):
		self.address = address

	def addPhone(self, number):
		self.phone = number

	def addEmail(self, email):
		self.email = email

	def addUrl(self, name, url):
		url = re.sub(',', '', url, re.UNICODE)
		self.urlList.append({
				"Website": name,
				"Url": url
			})

	def getStartupData(self):
		startupData = {
			"Name": self.name,
			"Teaser": self.teaser,
			"Description": self.description,
			"Address": self.address,
			"E-Mail": self.email,
			"Phone": self.phone,
			"Founding year": self.founding_year,
			"Web": self.urlList,
			"Founder": self.founder,
			"Finance": self.finance,
			"Investors": self.investors
		}
		return startupData