import csv
import os
import json


class Stats(object):

    def __init__(self):
        self.title = "" 
        self.key   = [] 
        self.stats = [] 
        self.path  = ''

    def load(self, path):
        self.path = path
        with open(path, 'r', newline="") as file:
            rows = [line.split(",") for line in file]
            for i,x in enumerate(rows):
                if i == 0:
                    self.title = x[0]
                    continue
                if i == 1:
                    self.key = x
                    continue

                stat = []
                for data in x:
                    stat.append(data.strip())

                self.stats.append(stat)
            self.stats.pop()

    def addStat(self, row):
        row = self.formatRow(row)
        self.stats.append(row)

    def save(self, path):
        if not path and not self.path:
            print('you must specify a destination')
            return
        
        save_path = path

        with open(save_path, 'w+', newline="") as f:
            writer = csv.writer(f)
            for row in self.stats:
                if not len(row) == 0:
                    writer.writerow(row)

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




class Defense(Stats):
    @staticmethod
    def keys(): 
        return ['ffum','int','ast','tkl','sk']


class Rushing(Stats):

    @staticmethod
    def keys(): 
        return ['lngtd','twoptm','yds','att','tds', 'lng', 'twopta']


class PuntReturns(Stats):
    @staticmethod
    def keys(): 
        return ['avg', "lng", "tds", "lng", "ret"]


class Passing(Stats):
    @staticmethod
    def keys(): 
        return ['ints', 'cmp', 'twoptm', 'yds', 'att', 'tds', "twopta"]


class Fumbles(Stats):
    @staticmethod
    def keys(): 
        return ['yds', 'trcv', 'rcv', 'lost', 'tot']

class Kicking(Stats):
    @staticmethod
    def keys(): 
        return ['fgyds', 'fga', 'xpa', 'totpfg', 'xpb', 'xpmade','fgm', 'xptot', 'xpmissed']

class KickReturns(Stats):
    @staticmethod
    def keys(): 
        return ['avg', 'lngtd', 'tds', 'lng', 'ret']

class Receiving(Stats):
    @staticmethod
    def keys(): 
        return ['twoptm', 'rec', 'yds', 'lngtd', 'tds', 'lng', 'twopta']

class Punting(Stats):
    @staticmethod
    def keys(): 
        return ['pts', 'yds', 'avg', 'i20', 'lng']

