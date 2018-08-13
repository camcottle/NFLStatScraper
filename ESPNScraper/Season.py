from .Team import Team


class Season(object):

    def __init__(self, **kwargs):
        self.year  = kwargs.get('year', 2017)
        self.teams = kwargs.get('teams', [])
        self.games = kwargs.get('games', [])

    def addTeam(self, team):
        self.teams.append(Team(**team))

    def addGame (self, **kwargs):
        self.games.append({
            "id": kwargs.get('id', 0),
            "home": kwargs.get('home', None),
            "away": kwargs.get('away', None),
            "week": kwargs.get("week", 0),
            "season_type": kwargs.get('season_type', 2),
            "result": kwargs.get('result', None)
        })

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

