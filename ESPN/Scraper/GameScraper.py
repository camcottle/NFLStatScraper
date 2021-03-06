import urllib.request
from bs4 import BeautifulSoup
import re

class Game(object):

    def __init__(self, game_id, side=0):
        self.game_id = game_id
        self.side = side
        self.host = "http://www.espn.com/nfl/boxscore"
        self.path = "?gameId={}"

        self.players = {}

    def scrape(self):
        html = self.sendRequest()
        document = BeautifulSoup(html.decode('utf-8'), 'lxml')
        boxscores = document.find_all(id=re.compile('^gamepackage-[a-z]+$'));

        stats = [
            'passing',
            'rushing',
            'receiving',
            'fumbles',
            'defensive',
            'interceptions',
            'kicking',
            'punting'
        ]
        for boxscore in boxscores:
            stat = boxscore.get('id').split('-')[1]
            if not stat in stats:
                continue

            team = boxscore.find_all('tbody')[self.side]
            for player in team.find_all('tr'):
                player_stats = {}
                current_player = None
                if 'highlight' in player.get('class', []):  
                    continue
                if len(player.find_all('td')) <= 1:
                    continue
                for stat_data in player.find_all('td'):
                    stat_column = stat_data.get('class', [])[0];
                    if stat_column == 'name':
                        if stat_data.a:
                            link = stat_data.a.get("href")
                        player_name = stat_data.span.get_text()
                        if link and re.search('[0-9]{3,7}', link):
                            current_player = re.search('[0-9]{3,7}', link).group(0)
                        if not self.hasPlayer(current_player):
                            self.addPlayer(player_name, current_player)

                        continue
                    player_stats[stat_column] = stat_data.get_text()
                    player_stats['game_id']   = self.game_id

                self.addStat(current_player, stat, player_stats);

    def addPlayer(self, player_name, player_id):
        self.players[player_id] = {
            "name": player_name,
            "id": player_id,
            "stats": {}    
        }

    def getPlayer(self, player_id):
        for player in self.players:
            if player == player_id:
                return self.players[player]
        return False

    def hasPlayer(self, player_id):
        for player in self.players:
            if player == player_id:
                return True

        return False

    def addStat(self, player_id, stat, player_stats):
        if not stat in self.players[player_id]['stats']:
            self.players[player_id]['stats'][stat] = []

        if "qbr" in player_stats:
            del player_stats['qbr']

        self.players[player_id]['stats'][stat].append(player_stats) 
        pass

    def sendRequest(self):
        path = self.path.format(self.game_id)
        return urllib.request.urlopen(self.host + path).read();