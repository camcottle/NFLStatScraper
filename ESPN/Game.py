import urllib.request
from bs4 import BeautifulSoup
import re


class Game(object):

    def __init__(self, **kwargs):
        self.id  = kwargs.get('id', 0)
        self.home = kwargs.get('home', None)
        self.away = kwargs.get('away', None)
        self.week = kwargs.get("week", 0)
        self.seasontype = kwargs.get('seasontype', 2)
        self.season = kwargs.get('season', 2018)
        self.parseResult(kwargs.get('result', None))

    def toDict(self): 
        return {
            "id": self.id,
            "home": self.home,
            "away": self.away,
            "week": self.week,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "seasontype": self.seasontype,
            "season": self.season,
        }

    def parseResult(self, result_string): 
        scores = result_string.split(",");
        if len(scores) == 1 and scores[0] in ["Canceled", "Postponed"]:
            self.home_score = 0
            self.away_score = 0
            return

        self.home_score = re.search('[0-9]+', scores[1]).group(0)
        self.away_score = re.search('[0-9]+', scores[0]).group(0)
        
    def addStat(self, stat_type, data):
        if not stat_type in self.stats:
            self.stats[stat_type] = []

        self.stats[stat_type].append(data)

    def getStats(self, stat_type):
        
        if not self.stats[stat_type]:
            return False

        return self.stats[stat_type]