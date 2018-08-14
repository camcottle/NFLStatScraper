import urllib.request
from bs4 import BeautifulSoup
import re


class Schedule(object):

    def __init__(self, year):
        self.year = year
        self.host = "http://www.espn.com/nfl/schedule/"
        self.path = "_/week/{}/year/{}/seasontype/{}"

        self.teams = []
        self.games = []


    def scrape(self):
        html = self.sendRequest(self.current_week, self.season_type)
        document = BeautifulSoup(html, 'html.parser');

        self.getTeams(document)
        self.getGames(document)

    def getPreSeason(self):
        self.season_type = 1
        self.current_week = 1

        while self.current_week <= 5:
            self.scrape()
            self.current_week += 1
            pass

    def getRegularSeason(self):
        self.season_type = 2
        self.current_week = 1

        while self.current_week <= 17:
            self.scrape()
            self.current_week += 1
            pass

    def getPostSeason(self):
        self.season_type = 3
        self.current_week = 1

        while self.current_week <= 5:
            self.scrape()
            self.current_week += 1
            pass

    def getGames(self, document):
        for table in document.find_all('table', class_='schedule'):
            schedule = table.find_all('tbody')
            if not len(schedule):
                continue
            for game in schedule[0].find_all('tr'):
                current_game = {}
                for idx, column in enumerate(game.find_all("td")):
                    if idx == 0:
                        team = column.find_all('abbr')[0]
                        current_game['away'] = team.contents[0]
                    if idx == 1:
                        team = column.find_all('abbr')[0]
                        current_game['home'] = team.contents[0]
                    if idx == 2: 
                        data   = column.find_all('a')[0]
                        link   = data.get('href') 
                        result = data.contents[0]
                        current_game["id"] = re.search('[0-9]{9}', link).group(0)
                        current_game["result"] = result

                current_game['week'] = self.current_week
                current_game['seasontype'] = self.season_type
                self.games.append(current_game)

    def getTeams(self, document):
        schedules = document.find_all('table', class_='schedule')
        for schedule in schedules:
            teams = schedule.find_all("abbr")
            
            for team in teams:
                abbr      = team.contents[0]
                team_name = team.get('title')

                self.teams.append({
                    'abbr': abbr,
                    'name': team_name
                })

    def sendRequest(self, week=1, seasontype=2):
        path = self.path.format(week, self.year, seasontype)
        return urllib.request.urlopen(self.host + path).read();