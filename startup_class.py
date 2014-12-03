class Startup(object):
	name = ""
	description = ""
	teaser =""
	founding_year = 0
	founder = []

	def __init__(self, name, description, founding_year):
		self.name = name
		self.description = description
		self.founding_year = founding_year

	def addTeaser (self, teaser):
		self.teaser = teaser

	def getStartupData(self):
		startupData = [{
			"name": self.name,
			"teaser": self.teaser,
			"description": self.description,
			"Founding year": self.founding_year,
			"Founder": self.founder
		}]
		return startupData