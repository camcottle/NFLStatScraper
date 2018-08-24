from .Player import Player


class Team(object):

    def __init__(self, **kwargs):
        self.abbr    = kwargs.get('abbr', None)
        self.name    = kwargs.get('name', '')
        self.players = kwargs.get('players', [])

    def toDict(self):
        return {
            "name": self.name,
            "abbr": self.abbr
        }

    def addPlayer(self, player):
        if not self.hasPlayer(player['id']):
            self.players.append(Player(**player))

    def hasPlayer(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return True
        return False

    def listPlayers(self):
        return self.players

    def getPlayer(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player

