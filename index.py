import ESPN
import csv
import os
import time

years = [
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
    "2000", 
    # "1999", 
    # "1998", 
    # "1997", 
    # "1996", 
    # "1995", 
]
for year in years:
    start_time = time.time()
    print("starting {}".format(year))
    schedule = ESPN.Schedule(year);

    # print('getPreSeason')
    schedule.getPreSeason()
    schedule.getRegularSeason()

    season_deets = {"year": year}
    season = ESPN.Season(**season_deets)
    for team in schedule.teams:
        if not season.hasTeam(team['abbr']):
            season.addTeam(team)

    for game in schedule.games:
        season.addGame(**game)


    for game in season.listGames():
        print(game['id'])
        home_game = ESPN.Game(game['id'])
        home_game.scrape()

        for stats in home_game.getHomeTeam():
            player = stats
            if not season.getTeam(game['home']).hasPlayer(player):
                season.getTeam(game['home']).addPlayer({
                    "name": player['name'],
                    "id": player['id'],
                })
            season.getTeam(game['home']).getPlayer(player['id']).addStat(player['stat_type'], player['stat'])

        for stats in home_game.getAwayTeam():
            player = stats
            if not season.getTeam(game['away']).hasPlayer(player):
                season.getTeam(game['away']).addPlayer({
                    "name": player['name'],
                    "id": player['id'],
                })
            season.getTeam(game['away']).getPlayer(player['id']).addStat(player['stat_type'], player['stat'])

    
    if not os.path.exists('seasons/' + year):
        os.mkdir('seasons/' + year)
    # Save to CSVs
    if not os.path.exists('seasons/' + year + "/teams"):
        os.mkdir('seasons/' + year + "/teams")

    with open('seasons/' + year + "/games.csv", "w", newline="") as file:
        games = season.listGames()
        keys = games[0].keys()

        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(games)


    for team in season.listTeams():
        if not os.path.exists('seasons/' + year + "/teams/" + team.name):
            os.mkdir('seasons/' + year + "/teams/" + team.name)
        
        for player in team.listPlayers():
            if not os.path.exists('seasons/' + year + "/teams/" + team.name + "/" + player.name):
                os.mkdir('seasons/' + year + "/teams/" + team.name + "/" + player.name)
        
            for stat in player.listStats():
                with open('seasons/' + year + "/teams/" + team.name + "/" + player.name + "/" + stat + ".csv", "w", newline="") as file:
                    player_stats = player.listStats()[stat]

                    keys = player_stats[0].keys()

                    writer = csv.DictWriter(file, keys)
                    writer.writeheader()
                    writer.writerows(player_stats)
                file.close()

    time_taken = (time.time() - start_time)

    print("completed {} in {}".format(year, time_taken))
    time.sleep(60)
