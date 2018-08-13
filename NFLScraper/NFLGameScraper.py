import urllib.request
import re
import csv
import json
import os
import stats
from bs4 import BeautifulSoup

class NFLGameScraper(object): 
    
    # Initialize Team
    def __init__(self, game_id, year):
        self.year    = year
        self.game_id = game_id

        self.paths = [
            "schedule",
            "roster"
        ]

        self.games   = []
        self.players = []
        self.stats   = {}

    def scrape(self):

        # prior to the 2008 season NFL used XML instead of JSON
        # so we can't rely on that
        if(self.year <= 2008):
            return self.legacyScraper()
        
        # read the response, send it to be processed
        data = self.sendRequest().read()
        self.processData(data)

    # We will build this out later
    def legacyScraper(self):
        pass

    # Take the data from the request and normalize it
    def processData(self, html):
        data = json.loads(html.decode('utf-8'))
        sides = [data[str(self.game_id)]['home'], data[str(self.game_id)]['away']]

        for side in sides:
            for stat_name in side['stats']:

                # we aren't tracking teams at this point 
                if stat_name == 'team':
                    continue

                # check if the proper list data exists, if not create an empty list 
                if not self.stats.get(stat_name):
                    self.stats[stat_name] = list()

                # normalize the data
                stats = self.normalizeData(side['stats'][stat_name])
                self.stats[stat_name] = stats

    def normalizeData(self, data):
        # create an empty list
        stats = list()
        player_ids = data.keys()

        for player_id in player_ids:
            self.players.append(player_id)
            player_data = data[player_id]

            if type(player_data) == type({}):
                player_data['id']        = self.game_id
                player_data['player_id'] = player_id
                player_data['year']      = self.year
                
                stats.append(player_data)
        
        return stats

    # prepare and send the request to the NFL website
    def sendRequest(self):
        url = "http://www.nfl.com/liveupdate/game-center/{}/{}_gtd.json"
        url = url.format(self.game_id, self.game_id)

        # Return the response
        return urllib.request.urlopen(url)