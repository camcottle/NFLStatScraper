from classes import Request
from classes import Season
from classes import Game
import codecs 
import re
import csv
import os
import time
import json

# scraper = Request("http://www.nfl.com/teams/profile?team=MIA")
team_list   = []
games_list  = []
player_data = []
rows        = {}

class Teams(object):

    def __init__(self, team, season=2017, type="REG"):


        self.team = team;
        self.season = season;
        self.type = type;

    @staticmethod
    def scrape(team):
        paths = [
            "profile",
            "schedule",              
            "roster",              
        ];

        years = [
            2008,
            2009,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
        ]
        for year in years: 
            for path in paths:
                request = Request("http://www.nfl.com/teams/" + path + 
                    "?team=" + team +
                    "&season=" + str(year) + 
                    "&seasonType=REG")
                if not request:
                    continue
                for link in request.response_html.find_all("a"):
                    url = str(link.get('href'))
                    if re.search('/gamecenter', url):
                        if not re.search('/watch', url):
                            games_list.append(url)
                        continue
                    elif re.search('/teams/profile', url):
                        team_list.append(url)
                    elif re.match('/player', url):
                        player_data.append(url)

        with open("teams.csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for row in set(team_list):
                writer.writerow([row])

        with open("games.csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for row in set(games_list):
                writer.writerow([row])

        with open("player.csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for row in set(player_data):
                writer.writerow([row])
class GameStats(object):

    def __init__(self, csv_path):
        self.title = ""
        self.key   = []
        self.stats = []

        with open(csv_path, 'r', newline="") as f:
            rows = [line.split(",") for line in f]
            for i,x in enumerate(rows):
                if i == 0:
                    self.title = x[0]
                    continue
                if i == 1:
                    self.key = x
                    continue
                self.stats.append(x)
            self.stats.pop()



    def displayStats(self):
        columns = 0
        column_widths = []

        merged = list(self.stats)
        merged.append(self.key)
        
        for row in merged: 
            if len(row) > columns:
                columns = len(row)
            for index, data in enumerate(row):
                if len(column_widths) <= index:
                    column_widths.append(0)
                if column_widths[index] < len(data):
                    column_widths[index] = len(data)

        row_format = ""
        row_length = 0
        for width in column_widths:
            row_format += "{:>" + str(width+4) +"}"
            row_length += width + 4

        print(row_format.format(*self.key).strip())
        for key, stats in zip(self.key, self.stats[:len(self.stats)]):
            print("-" * row_length);
            print(row_format.format(*stats).strip())


    @staticmethod
    def scrape(path):
        request = Request("http://www.nfl.com/" + path)
        data = json.loads(request.response.decode('utf-8'))
        form = "{}" * (len(data["2017090700"])- 1)
        stats = data["2017090700"]["home"]["stats"]

        for index, section in enumerate(stats): 
            if section == "team":
                continue
            print(section)
            for i in stats[section]:
                var = i
                print(stats[section][i])

        # for table in request.response:
            # print(table)
            # rows = table.findChildren("tr", {"class": })

            # print(table)
        #     stat_table = []
        #     for row in rows:
        #         stat_row = []
        #         for data in row.findChildren("td"):
        #             if data.findChildren("a"):
        #                 # link = data.findChildren("a");
        #                 stat_row.append(data.findChildren("a")[0].contents[0])
        #                 continue
        #             if data.findChildren("div"):
        #                 # link = data.findChildren("div");
        #                 stat_row.append(data.findChildren("div")[0].contents[0])
        #                 continue
        #             if not len(data.contents):
        #                 continue
        #             stat_row.append(data.contents[0])

        #         stat_table.append(stat_row)
        #     stats.append(stat_table)
        
        # if not os.path.exists("players/" + name):
        #     os.makedirs("players/" + name)
        # for stat in stats: 
        #     stat_name = str(stat[0][0]).lower()
        #     print(stat_name, name)
        #     with open('players/' + name + '/' + stat_name.replace(' ', "_") + '.csv', 'w+', newline="") as f:
        #         writer = csv.writer(f)
        #         for row in stat[1:]:
        #             if not len(row) == 0:
        #                 writer.writerow(row)




class PlayerStats(object):

    def __init__(self, csv_path):
        self.title = ""
        self.key   = []
        self.stats = []

        with open(csv_path, 'r', newline="") as f:
            rows = [line.split(",") for line in f]
            for i,x in enumerate(rows):
                if i == 0:
                    self.title = x[0]
                    continue
                if i == 1:
                    self.key = x
                    continue
                self.stats.append(x)
            self.stats.pop()



    def displayStats(self):
        columns = 0
        column_widths = []

        merged = list(self.stats)
        merged.append(self.key)
        
        for row in merged: 
            if len(row) > columns:
                columns = len(row)
            for index, data in enumerate(row):
                if len(column_widths) <= index:
                    column_widths.append(0)
                if column_widths[index] < len(data):
                    column_widths[index] = len(data)

        row_format = ""
        row_length = 0
        for width in column_widths:
            row_format += "{:>" + str(width+4) +"}"
            row_length += width + 4

        print(row_format.format(*self.key).strip())
        for key, stats in zip(self.key, self.stats[:len(self.stats)]):
            print("-" * row_length);
            print(row_format.format(*stats).strip())


    @staticmethod
    def scrape(path):
        request = Request("http://www.nfl.com/" + path)
        name = request.response_html.find("span", {"class": "player-name"})
        name = str(name.contents[0]).strip().lower().replace(' ', "_")

        stats = [];

        for table in request.response_html.find_all("table"):
            rows = table.findChildren("tr")
            stat_table = []
            for row in rows:
                stat_row = []
                for data in row.findChildren("td"):
                    if data.findChildren("a"):
                        # link = data.findChildren("a");
                        stat_row.append(data.findChildren("a")[0].contents[0])
                        continue
                    if data.findChildren("div"):
                        # link = data.findChildren("div");
                        stat_row.append(data.findChildren("div")[0].contents[0])
                        continue
                    if not len(data.contents):
                        continue
                    stat_row.append(data.contents[0])

                stat_table.append(stat_row)
            stats.append(stat_table)
        
        if not os.path.exists("players/" + name):
            os.makedirs("players/" + name)
        for stat in stats: 
            stat_name = str(stat[0][0]).lower()
            print(stat_name, name)
            with open('players/' + name + '/' + stat_name.replace(' ', "_") + '.csv', 'w+', newline="") as f:
                writer = csv.writer(f)
                for row in stat[1:]:
                    if not len(row) == 0:
                        writer.writerow(row)

        # with open(self.name + "/stats.csv", 'w', newline="") as f:
        #     writer = csv.writer(f)
        #     for rows in stats:
        #         print(len(row))
        #         for row in rows:
        #             if len(row) == 0:
        #                 continue
        #             writer.writerow(row)

# player = PlayerStats('players/aaron_rodgers_defensive.csv')
# player.displayStats()

# for index, path in enumerate(paths):
#     percentage = ((index + 1)/len(paths)) * 100
#     os.system('clear');
#     print("Scraping players: " + str(round(percentage, 2)) + "% Completed   (" + str(index) + " of " + str(len(paths)) + ")")
#     print("Current player path: " + path)
#     player = PlayerScraper(path)
#     player.scrape()
#     time.sleep(2)



# teams = [
#     'SF',
#     'NYJ',
#     'PIT',
#     'WAS',
#     'KC',
#     'IND',
#     'BAL',
#     'OAK',
#     'DAL',
#     'TEN',
#     'CAR',
#     'NE',
#     'SEA',
#     'HOU',
#     'DET',
#     'CLV',
#     'BUF',
#     'GB',
#     'LAC',
#     'MIA',
#     'JAX',
#     'ATL',
#     'DEN',
#     'MIN',
#     'PHI',
#     'TB',
#     'CIN',
#     'CHI',
#     'NO',
#     'NYG',
#     'ARZ',
# ]
# for team in teams:
#     Teams.scrape(team);
#     da_team.scrape()
    # print(team);

# players = []
# with open("player.csv", 'r', newline="") as f:
#     for line in f:
#         players.append(line.strip())

# for index, player in enumerate(players):
#     percentage = ((index + 1)/len(players)) * 100
#     os.system('clear');
#     print("Scraping players: " + str(round(percentage, 2)) + "% Completed   (" + str(index) + " of " + str(len(players)) + ")")
#     print("Current player path: " + player)
#     PlayerStats.scrape(player)


games = ["liveupdate/game-center/2017090700/2017090700_gtd.json"]
for game in games:
    GameStats.scrape(game);

# # for link in scraper.response_html.find_all('a'):
# #     url = str(link.get('href'))
# #     if re.search('/gamecenter', url):
# #         if not re.search('/watch', url):
# #             games_list.append(url)
# #         continue
# #     elif re.search('/teams/profile', url):
# #         team_list.append(url)
# #     elif re.match('^[a-z^/:]+$', url):
# #         player_data.append(url)

# with open("teams.csv", 'w', newline="") as f:
#     writer = csv.writer(f)
#     for row in set(team_list):
#         writer.writerow(list([row, False]))

# with open("games.csv", 'w', newline="") as f:
#     writer = csv.writer(f)
#     for row in set(games_list):
#         writer.writerow(list([row, False]))

# with open("player.csv", 'w', newline="") as f:
#     writer = csv.writer(f)
#     for row in set(player_data):
#         writer.writerow(list([row, False]))

# rows[0] = ["id", "year", "home", "away", "season", "path"];

# season = Season()
# for game_url in games_list:
#     game = Game()
#     game.newFromURL(game_url)

#     season.addGame(game)

# season.listGames();
# season.toCSV();
    # game_id = re.search('(\d+)', game).group(0)
    # year = re.search('(\d{4})', game).group(0)
    # teams = re.search('(\w+@\w+)', game).group(0)
    # game_meta = re.search('([A-Z]+[0-9]+)', game).group(0)

    # season = re.search('([A-Z]+)', game_meta).group(0)
    # number = re.search('([0-9]+)', game_meta).group(0)

    # home, away = teams.split('@');
    # row = [game_id, year, home, away, season, game]
    # rows[game_id] = row;
    
# new_team_list = []
# for team in team_list:
#     current_team = re.search('team=([A-Z]{3})', team);
#     if not current_team:
#         continue
#     new_team_list.append([current_team.group(1), team])

# team_list = new_team_list;    

    
    
