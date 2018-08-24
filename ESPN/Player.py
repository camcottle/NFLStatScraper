import urllib.request
from bs4 import BeautifulSoup
import re


class Player(object):

    def __init__(self, **kwargs):
        self.id       = kwargs.get('id', None)
        self.name     = kwargs.get('name', '')
        self.position = kwargs.get('position', '')
        self.stats    = {}

        stats         = kwargs.get('stats', {})
        
        for stat in stats:
            for line in stats[stat]:
                self.addStat(stat, line)

    def toDict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
        }

    def listStats(self): 
        return self.stats;
        
    def addStat(self, stat_type, data):
        if not stat_type in self.stats:
            self.stats[stat_type] = []

        self.stats[stat_type].append(data)

    def getStats(self, stat_type):
        
        if not self.stats[stat_type]:
            return False

        return self.stats[stat_type]