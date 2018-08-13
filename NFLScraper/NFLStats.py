import csv
import os
import json


class NFLStats(object):

    def __init__(self):
        self.title = "" 
        self.key   = [] 
        self.stats = [] 
        self.path  = ''

    def load(self, path):
        self.path = path
        if not os.path.exists(path):
            # print("doesn't exist")
            with open(path, 'w', newline="") as file: 
                pass
        with open(path, 'r', newline="") as file:
            rows = [line.split(",") for line in file]
            for i,x in enumerate(rows):

                stat = []
                for data in x:
                    stat.append(data.strip())

                self.stats.append(stat)
            file.close()
                

    def addStat(self, row):
        row = self.formatRow(row)
        self.stats.append(row)

    def save(self, path):
        if not path and not self.path:
            print('you must specify a destination')
            return


        with open(self.path, 'w', newline="") as f:
            writer = csv.writer(f)
            for row in self.stats:
                if not len(row) == 0:
                    writer.writerow(row)
            f.close()

    def displayTable(self):
        if not self.stats:
            print('no data loaded');
            return 

        columns = 0
        column_widths = []

        stats = self.stats;

        if self.keys():
            stats = [self.keys()] + self.stats

        for row in stats: 
            if len(row) > columns:
                columns = len(row)
            for index, data in enumerate(row):
                if len(column_widths) <= index:
                    column_widths.append(0)
                if column_widths[index] < len(str(data)):
                    column_widths[index] = len(str(data))

        row_format = ""
        row_length = 0
        for width in column_widths:
            row_format += "{:>" + str(width+3) +"}"
            row_length += width + 3

        for stat in stats:
            print("-" * row_length);
            print(row_format.format(*stat).strip())

    def formatRow(self, stat):
        
        formatted_row = []
        for stat_item in self.keys():
            if not stat.get(stat_item): 
                formatted_row.append(0);
                continue
            formatted_row.append(stat.get(stat_item));

        return formatted_row




class NFLDefenseStats(NFLStats):
    @staticmethod
    def keys(): 
        return ['id', 'player_id', 'name', "side", 'ffum', 'int', 'ast', 'tkl', 'sk']


class NFLRushingStats(NFLStats):

    @staticmethod
    def keys(): 
        return ['id', 'player_id', 'name', "side", 'lngtd', 'twoptm', 'yds', 'att', 'tds', 'lng', 'twopta']


class NFLPuntReturnsStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'avg', "lng", "tds", "lng", "ret"]


class NFLPassingStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'ints', 'cmp', 'twoptm', 'yds', 'att', 'tds', "twopta"]


class NFLFumblesStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'yds', 'trcv', 'rcv', 'lost', 'tot']

class NFLKickingStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'fgyds', 'fga', 'xpa', 'totpfg', 'xpb', 'xpmade','fgm', 'xptot', 'xpmissed']

class NFLKickReturnsStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'avg', 'lngtd', 'tds', 'lng', 'ret']

class NFLReceivingStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'twoptm', 'rec', 'yds', 'lngtd', 'tds', 'lng', 'twopta']

class NFLPuntingStats(NFLStats):
    @staticmethod
    def keys(): 
        return [ 'id', 'player_id', 'name', "side", 'pts', 'yds', 'avg', 'i20', 'lng']

