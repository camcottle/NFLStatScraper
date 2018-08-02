import re

class Game(object): 
    # Initialize Team
    def __init__(self):
        self.data = {}
        return
    
    def newFromURL(self, url):
        self.id = re.search('(\d+)', url).group(0)
        self.year = re.search('(\d{4})', url).group(0)
        
        game_meta = re.search('([A-Z]+[0-9]+)', url).group(0)
        
        self.season = re.search('([A-Z]+)', game_meta).group(0)
        self.game = re.search('([0-9]+)', game_meta).group(0)

        teams = re.search('(\w+@\w+)', url).group(0)
        self.home, self.away = teams.split('@');

    def getTeams(self): 
        return (self.home, self.away);

    def toList(self):
        return [
            self.id,
            self.year,
            self.game,
            self.home,
            self.away
        ]