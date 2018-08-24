import ESPN
import csv
import os
import time

class Scraper(object):

    def __init__(self):
        self.years = [
            "2017", 
            "2016", 
            "2015", 
            "2014", 
            "2013", 
            "2012", 
            "2011",
            "2010", 
            "2009", 
            "2008", 
            "2007", 
            "2006", 
            "2005", 
            "2004", 
            "2003", 
            "2002", 
            "2001",  
        ]
        self.current = 0
        self.games   = []
        self.player_ids = set()

    def hasSeasons(self):
        if self.current < len(self.years):
            return True

        return False

    def nextSeason(self):
        if self.hasSeasons():
            self.current = self.current + 1
            return

        return False

    def scrapeSeason(self):
        year     = self.years[self.current]
        schedule = ESPN.ScheduleScraper(year)
        schedule.getPreSeason()
        schedule.getRegularSeason()
        schedule.getPostSeason()

        for game in schedule.games:
            game['season'] = self.years[self.current]
            game_obj = ESPN.Game(**game)
            self.games.append(game_obj)

        # season = ESPN.season({"year": year})

        # for team in schedule.teams:
        #     if not season.hasTeam(team['abbr']):
        #         season.addTeam(team)

        # for game in schedule.games:
        #     season.addGame(game)
        #     self.append(game)


        # for game in season.listGames():
        #     game_dict = game.toDict();
        #     home_game = ESPN.GameScraper(game_dict['id'])
        #     home_game.scrape()

        #     for stats in home_game.getHomeTeam():
        #         player = stats
        #         if not season.getTeam(game_dict['home']).hasPlayer(player):
        #             season.getTeam(game_dict['home']).addPlayer({
        #                 "name": player['name'],
        #                 "id": player['id'],
        #             })
        #         season.getTeam(game_dict['home']).getPlayer(player['id']).addStat(player['stat_type'], player['stat'])

        #     for stats in home_game.getAwayTeam():
        #         player = stats
        #         if not season.getTeam(game_dict['away']).hasPlayer(player):
        #             season.getTeam(game_dict['away']).addPlayer({
        #                 "name": player['name'],
        #                 "id": player['id'],
        #             })
        #         season.getTeam(game_dict['away']).getPlayer(player['id']).addStat(player['stat_type'], player['stat'])

    # def scrapePlayers(): 

        # for index, team in enumerate(season.listTeams()):
        #     for player in team.listPlayers():
        #         os.system('clear')
        #         print('Team: {}    [{}/{}]'.format(team.name, index+1, len(season.listTeams())))
        #         print("Current Player: {}".format(player.name))
        #         scraper = ESPN.PlayerScraper(player.id)
        #         player_details = scraper.scrape()
        #         players.append(player_details)


scraper = Scraper()
while scraper.hasSeasons():
    print(scraper.years[scraper.current])
    scraper.scrapeSeason()
    scraper.nextSeason()

with open('games.csv', 'w', newline="") as file:
    keys   = scraper.games[0].toDict().keys()
    writer = csv.DictWriter(file, ['id', "home", "away", "home_score", "away_score", "week", "season", "seasontype"])

    games = []

    for game in scraper.games:
        games.append(game.toDict())

    writer.writeheader()
    writer.writerows(games)



















# for year in years:
#     start_time = time.time()
#     schedule   = ESPN.ScheduleScraper(year);
#     players    = []
#     # print('getPreSeason')
#     schedule.getPreSeason()
#     schedule.getRegularSeason()

#     season_deets = {"year": year}
#     season = ESPN.Season(**season_deets)
#     for team in schedule.teams:
#         if not season.hasTeam(team['abbr']):
#             season.addTeam(team)

#     for game in schedule.games:
#         season.addGame(game)


#     for game in season.listGames():
#         game_dict = game.toDict();
#         home_game = ESPN.GameScraper(game_dict['id'])
#         home_game.scrape()

#         for stats in home_game.getHomeTeam():
#             player = stats
#             if not season.getTeam(game_dict['home']).hasPlayer(player):
#                 season.getTeam(game_dict['home']).addPlayer({
#                     "name": player['name'],
#                     "id": player['id'],
#                 })
#             season.getTeam(game_dict['home']).getPlayer(player['id']).addStat(player['stat_type'], player['stat'])

#         for stats in home_game.getAwayTeam():
#             player = stats
#             if not season.getTeam(game_dict['away']).hasPlayer(player):
#                 season.getTeam(game_dict['away']).addPlayer({
#                     "name": player['name'],
#                     "id": player['id'],
#                 })
#             season.getTeam(game_dict['away']).getPlayer(player['id']).addStat(player['stat_type'], player['stat'])

#     for index, team in enumerate(season.listTeams()):
#         for player in team.listPlayers():
#             os.system('clear')
#             print('Team: {}    [{}/{}]'.format(team.name, index+1, len(season.listTeams())))
#             print("Current Player: {}".format(player.name))
#             scraper = ESPN.PlayerScraper(player.id)
#             player_details = scraper.scrape()
#             players.append(player_details)

#     with open('players.csv', 'w', newline="") as file:
#         keys = players[0].keys()

#         writer = csv.DictWriter(file, keys)
#         writer.writeheader()
#         writer.writerows(players)

#     if not os.path.exists('seasons/' + year):
#         os.mkdir('seasons/' + year)
#     # Save to CSVs
#     if not os.path.exists('seasons/' + year + "/teams"):
#         os.mkdir('seasons/' + year + "/teams")

#     with open('seasons/' + year + "/games.csv", "w", newline="") as file:
#         games = season.listGames()
#         keys = games[0].toDict().keys()
#         games_dict = []
#         for game in games:
#             games_dict.append(game.toDict())

#         writer = csv.DictWriter(file, keys)
#         writer.writeheader()
#         writer.writerows(games_dict)


#     for team in season.listTeams():
#         if not os.path.exists('seasons/' + year + "/teams/" + team.name):
#             os.mkdir('seasons/' + year + "/teams/" + team.name)
        
#         for player in team.listPlayers():
#             if not os.path.exists('seasons/' + year + "/teams/" + team.name + "/" + player.name):
#                 os.mkdir('seasons/' + year + "/teams/" + team.name + "/" + player.name)
        
#             for stat in player.listStats():
#                 with open('seasons/' + year + "/teams/" + team.name + "/" + player.name + "/" + stat + ".csv", "w", newline="") as file:
#                     player_stats = player.listStats()[stat]

#                     keys = player_stats[0].keys()

#                     writer = csv.DictWriter(file, keys)
#                     writer.writeheader()
#                     writer.writerows(player_stats)
#                 file.close()

#     time_taken = (time.time() - start_time)

#     print("completed {} in {}".format(year, time_taken))
