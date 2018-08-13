import urllib.request
import re
import csv
import os
from bs4 import BeautifulSoup

class NFLTeamScraper(object): 
    
    # Initialize Team
    def __init__(self, team, year):
        self.year   = year
        self.season = "REG"
        self.team   = team

        self.patterns = {
            "games": "/gamecenter",
            "players": '/player/'
        }

        self.paths = [
            "schedule",
            "roster"
        ]

        self.games   = []
        self.players = []

    def scrape(self):
        for path in self.paths:
            # read the response and process it
            data = self.sendRequest(path).read()
            self.processData(data);

    def processData(self, html):
        # convert the data into something python can read easier
        document = BeautifulSoup(str(html), "html.parser")
        # iterate through all links on the current page
        for link in document.find_all("a"):
            # Get the current link destination
            url = link.get('href')
            # check to see if the link matches the patterns
            for pattern in self.patterns:
                if re.search(self.patterns.get(pattern), url):
                    data = getattr(self, pattern)
                    data.append(url)
                    setattr(self, pattern, data)

    # Export the search data to CSVs
    def save(self):
        for result in ["games", "players"]:
            # Check if file exists, otherwise don't 
            if not os.path.exists(result + ".csv"):
                with open(result + '.csv', 'w', newline= "") as f:
                    pass
            with open(result + ".csv", 'a', newline="") as f:
                writer = csv.writer(f)
                for row in getattr(self, result):
                    writer.writerow([row])

    # prepare the request data, send the request
    def sendRequest(self, path):
        url = "http://www.nfl.com/teams/{}?team={}&season={}&seasonType={}"
        url = url.format(path, self.team, self.year, "REG")
        return urllib.request.urlopen(url);