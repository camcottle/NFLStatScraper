import urllib.request
import re
import csv
import json
import os
import stats
from bs4 import BeautifulSoup

class NFLPlayerScraper(object): 
    
    # Initialize Team
    def __init__(self, player_id):
        self.player_id = player_id
        self.player_data = {}

    def scrape(self):
        # read the response, send it to be processed
        data = self.sendRequest()
        self.processData(data.read())
        print(self.player_data)

    # We will build this out later
    def legacyScraper(self):
        pass

    # Take the data from the request and normalize it
    def processData(self, html):
        player_data = BeautifulSoup(html, 'html.parser')
        player_info = player_data.find_all("div", class_="player-info")[0]

        player_name   = player_info.find_all("span", class_="player-name")[0].contents[0]
        self.player_data['id'] = self.player_id
        self.player_data['name'] = player_name.strip()
        # player_number = player_info.find_all("span", class_="player-number")[0].content
        player_number = player_info.find_all("span", class_="player-number")
        if not player_number:
            return

        player_number = player_number[0].contents[0].split()

        self.player_data['number'] = player_number[0]
        self.player_data['position'] = player_number[1]



    # prepare and send the request to the NFL website
    def sendRequest(self):
        url = "http://www.nfl.com/players/profile?id={}"
        url = url.format(self.player_id)
        # Return the response
        return urllib.request.urlopen(url)