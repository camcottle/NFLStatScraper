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

    def addStats(self, rows):
        self.stats = [rows] + self.stats

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

        for row in self.stats[2:]: 
            if len(row) > columns:
                columns = len(row)
            for index, data in enumerate(row):
                if len(column_widths) <= index:
                    column_widths.append(0)
                if column_widths[index] < len(data):
                    column_widths[index] = len(data)

        row_format = ""
        row_length = 0
        for width in column_widths:
            row_format += "{:>" + str(width+4) +"}"
            row_length += width + 4

        for stats in self.stats[:len(self.stats)]:
            print("-" * row_length);
            print(row_format.format(*stats).strip())



stats = Stats()
stats.load('players/alex_smith/defensive.csv')
stats.addStats(['2018','Washington Redskins',"15",'2','2','0','0.0','0','0',"--","--","--",'0.0',"--"])
os.system('clear')
stats.save('alex_smith_updated.csv');
stats.displayTable()