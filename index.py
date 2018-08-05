import scraper
import csv

years = [
    "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2016",
    "2017"
]

for year in years:
    for team in scraper.Teams:
        team = scraper.NFLTeamScraper(team, year)
        team.scrape()
        team.save()

players = set()
games = set()
with open('players.csv', 'r', newline="") as file:
    rows = [line.split(",") for line in file]
    for row in rows:
        players.add(row[0].strip())

with open('games.csv', 'r', newline="") as file:
    rows = [line.split(",") for line in file]
    for row in rows:
        games.add(row[0].strip())

with open('players.csv', 'w', newline="") as file:
    writer = csv.writer(file)
    for row in players:
        writer.writerow([row])

with open('games.csv', 'w', newline="") as file:
    writer = csv.writer(file)
    for row in games:
        writer.writerow([row])
