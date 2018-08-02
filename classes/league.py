import re

class League(object): 

    # Initialize Team
    def __init__(self):
        self.year  = 2017
        self.teams = []

    def addTeam(self, team):
        self.teams.append(team);
