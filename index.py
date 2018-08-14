import ESPN
import csv
import os

year = "2017"
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
    home = game['home']
    away = game['away']
    home_game = ESPN.Game(game['id'], 1)
    home_game.scrape()
    for player in home_game.players:
        de_player = home_game.players[player]
        if not season.getTeam(home).hasPlayer(de_player['id']):
            season.getTeam(home).addPlayer({
                "name": de_player['name'],
                "id": de_player['id'],
                "stats": de_player['stats']
            })
        else:
            for stat_type in de_player['stats']:
                for line in de_player['stats'][stat_type]:
                    season.getTeam(home).getPlayer(de_player['id']).addStat(stat_type, line)

    away_game = ESPN.Game(game['id'], 0)
    away_game.scrape()
    for player in away_game.players:
        de_player = away_game.players[player]
        if not season.getTeam(away).hasPlayer(de_player['id']):
            season.getTeam(away).addPlayer({
                "name": de_player['name'],
                "id": de_player['id'],
                "stats": de_player['stats']
            })
        else:
            for stat_type in de_player['stats']:
                for line in de_player['stats'][stat_type]:
                    season.getTeam(away).getPlayer(de_player['id']).addStat(stat_type, line)

year = str(year)
if not os.path.exists('seasons/' + year):
    os.mkdir('seasons/' + year)
# Save to CSVs
if not os.path.exists('seasons/' + year + "/teams"):
    os.mkdir('seasons/' + year + "/teams")
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


# team = season.getTeam('KC')



# for player in team.listPlayers():
#     print("\n" + player.name)
#     for stat in player.listStats():
#         print("\t" + stat)
#         for line in player.listStats()[stat]:
#             print(line)
# for player in season.getTeam(season.listGames()[0]['home']).listPlayers():
    # print("\n" + player.name)
    # for stat in player.listStats():
        # print("    " + stat)

    # for stats in game.players[player]["stats"]:
    #     print("\t" + stats)
# for team in season.season.listTeams():
#     print(team.name)

# for game in season.season.listGames():
    # print(game['id'])
# print('getRegularSeason')
# season.getRegularSeason()
# # print('getPostSeason')
# # season.getPostSeason()

# print(season.games)

# season = {'year': 2017}
# season = ESPNScraper.Season(**season)

# season.addTeam({
#     "abbreviation": "NYJ",
#     "name": "New York Jets"
# })

# team = season.getTeam('NYJ')

# team.addPlayer({
#     "id": "00-000123",
#     "name": "Pedro Babaganoosh",
#     "position": "WR"
# })

# player = team.getPlayer("00-000123")
# player.addStat('defense', {
#     "game_id": "1000234",
#     "tackles": 15,
#     "sacks": 2,
#     "ffum": 2
# })
    
# print(season.listTeams()[0].listPlayers()[0].stats)



# for year in years:
#     for team in scraper.Teams:
#         team = scraper.NFLTeamScraper(team, year)
#         team.scrape()
#         team.save()

# players = set()
# games = set()
# csv_data = CSVHelper('testing.csv')


# def statType(stat_type):
#     if stat_type == 'kicking':
#         return scraper.NFLKickingStats()
    
#     if stat_type == 'receiving':
#         return scraper.NFLReceivingStats()
    
#     if stat_type == 'defense':
#         return scraper.NFLDefenseStats()
    
#     if stat_type == 'rushing':
#         return scraper.NFLRushingStats()
    
#     if stat_type == 'puntret':
#         return scraper.NFLPuntReturnsStats()
    
#     if stat_type == 'passing':
#         return scraper.NFLPassingStats()
    
#     if stat_type == 'fumbles':
#         return scraper.NFLFumblesStats()
    
#     if stat_type == 'kickret':
#         return scraper.NFLKickReturnsStats()
    
#     if stat_type == 'punting':
#         return scraper.NFLPuntingStats()

# player_ids = set()
# with open("games.csv", "r", newline="") as file:
#     lines = [line.split() for line in file]
#     print(len(lines))
#     count = 0
#     for row in lines:
#         count += 1
#         os.system('clear')
#         print((count/len(lines))*100);

#         search_id = re.search('/([0-9]{10})/', row[0]).group(1)
#         year      = re.search('/([0-9]{4})/', row[0]).group(1)
        
#         game = scraper.NFLGameScraper(search_id, int(year))
#         game.scrape();

#         player_ids = player_ids.union(set(game.players))
#         # print(player_ids    )

#         for stat in game.stats:
#             stats = statType(stat)
#             stats.load('stats/' + stat + '.csv')

#             for record in game.stats[stat]:
#                 stats.addStat(record)

#             stats.save('stats/' + stat + '.csv')
# file.close()


# with open("players.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     for id in player_ids:
#         writer.writerow([id])

# scraped = []
# with open("players.csv", "r", newline="") as file:
#     players = [line.split() for line in file]
#     for player_id in players:
#         player = scraper.NFLPlayerScraper(player_id[0])
#         player.scrape();
#         scraped.append(player.player_data)

# file.close()

# with open("player_details", "w", newline="") as file:
#     writer = csv.writer(file)
#     for player in scraped:
#         row = [
#             player['id'],
#             player['name']
#         ]

#         if player.position:
#             row.append(player['position'])

#         if player.number:
#             row.append(player['number'])

#         writer.writerow([row])


        # player_ids = player_ids.union(set(game.players))
        # # print(player_ids    )

        # for stat in game.stats:
        #     stats = statType(stat)
        #     stats.load('stats/' + stat + '.csv')

        #     for record in game.stats[stat]:
        #         stats.addStat(record)

        #     stats.save('stats/' + stat + '.csv')


































# files = os.listdir('stats')[:1]
# for file_name in files:
#     data = list() 
#     with open("stats/" + file_name, "r", newline="") as file: 
#         rows = [line.split() for line in file]
#         for row in rows:
#             data_row = []
#             columns  = [column.split(",") for column in row]
#             for column in columns:
#                 data_row.append(column)
#             data.append(data_row)    

#     with open("stats/" + file_name, "w", newline="") as file:
#         writer = csv.writer(file)
#         for row in data:
#             writer.writerow(row)

# with open('players.csv', 'r', newline="") as file:
#     rows = [line.split(",") for line in file]
#     for row in rows:
#         players.add(row[0].strip())

# with open('games.csv', 'r', newline="") as file:
#     rows = [line.split(",") for line in file]
#     for row in rows:
#         games.add(row[0].strip())

# with open('players.csv', 'w', newline="") as file:
#     writer = csv.writer(file)
#     for row in players:
#         writer.writerow([row])

# with open('games.csv', 'w', newline="") as file:
#     writer = csv.writer(file)
#     for row in games:
#         writer.writerow([row])
