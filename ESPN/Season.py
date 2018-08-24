from .Team import Team
from .Game import Game


class Season(object):

    def __init__(self, **kwargs):
        self.year  = kwargs.get('year', 2017)
        self.teams = kwargs.get('teams', [])
        self.games = kwargs.get('games', [])

    def addTeam(self, team):
        self.teams.append(Team(**team))

    def addGame (self, game):
        self.games.append(Game(**game))

    def listTeams(self):
        return self.teams

    def listGames(self):
        return self.games

    def hasTeam(self, team_abbr):
        for team in self.teams:
            if team.abbr == team_abbr:
                return True

        return False

    def getTeam(self, team_abbr):
        for team in self.teams:
            if team.abbr == team_abbr:
                return team

