import re
import csv

class Season(object): 

    # Initialize Team
    def __init__(self):
        self.year = 2017
        self.games = []

    def addGame(self, game):
        if self.findById(game.id):
            return
        self.games.append(game);        
    
    def findById(self, id):
        for game in self.games:
            if game.id == id:
                return game
        return False
    

    def listGames(self):
        games = []
        for game in self.games:
            games.append(game.toList());
        return games

    def toCSV(self):
        with open("season" + str(self.year) + ".csv", 'w', newline="") as f:
            writer = csv.writer(f)
            for row in self.listGames():
                writer.writerow(row);
