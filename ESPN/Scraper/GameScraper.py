import urllib.request
from bs4 import BeautifulSoup
import re

class Game(object):

    def __init__(self, game_id):
        self.game_id = game_id
        self.stats = []

    def scrape(self):
        html = self.sendRequest()
        document = BeautifulSoup(html.decode('utf-8'), 'lxml')
        stat_tables = document.find_all(id=re.compile('^gamepackage-[a-z]+$'));

        stat_tables = self.filterTables(stat_tables);

        for stat_type in stat_tables:
            for side, table in enumerate(stat_tables[stat_type].find_all('tbody')):

                self.stats = self.stats + (self.getStats(table, stat_type, side))

    def getHomeTeam(self):
        if not len(self.stats):
            self.scrape()

        return [stat for stat in self.stats if stat['side'] == 1]


    def getAwayTeam(self):
        if not len(self.stats):
            self.scrape()

        return [stat for stat in self.stats if stat['side'] == 0]

    def getStats(self, table, stat_type, home=0):
        stat_data = []

        for row in table.find_all('tr'):
            # Skip rows that have only one column or are highlighted
            # Highlighted rows don't have player information
            if 'highlight' in row.get('class', []) or len(row.find_all('td')) <= 1:
                continue

            player = {
                "id": None,
                "name": None,
                "side": home,
                "stat_type": stat_type,
                "stat": {}
            }
            for data in row.find_all('td'):

                stat_column = data.get('class', [])[0]
                
                if stat_column == 'qbr':
                    continue

                if stat_column == 'name':
                    if data.a:
                        link = data.a.get("href")
                    print(link)
                    player["id"]   = re.search('[0-9]{1,7}', link).group(0)
                    player["name"] = data.span.get_text()

                    continue

                player['stat'][stat_column] = data.get_text()

            player['stat']["game_id"] = self.game_id
            stat_data.append(player)

        return stat_data

    def filterTables(self, stat_tables):
        allowed_stats = [
            'passing',
            'rushing',
            'receiving',
            'fumbles',
            'defensive',
            'interceptions',
            'kicking',
            'punting'
        ]

        filtered_tables = {}

        for stat_table in stat_tables:
            stat = stat_table.get('id').split('-')[1]

            if stat in allowed_stats:
                filtered_tables[stat] = stat_table

        return filtered_tables

    def sendRequest(self):
        path = "http://www.espn.com/nfl/boxscore?gameId={}"
        return urllib.request.urlopen(path.format(self.game_id)).read();