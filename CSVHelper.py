import csv
import os

class CSVHelper(object):

    def __init__(path):
        print("called")
        # with open(path, 'r', newline="") as file:
        #     for row in [line.split() for line in file]:
        #         data = []
        #         for column in [line.split() for col in row]:
        #             data.append(column);
        #         print(data)
                

    def addStat(self, row):
        row = self.formatRow(row)
        self.stats.append(row)

    # def save(self, path):
    #     if not path and not self.path:
    #         print('you must specify a destination')
    #         return


    #     with open(self.path, 'w', newline="") as f:
    #         writer = csv.writer(f)
    #         for row in self.stats:
    #             if not len(row) == 0:
    #                 writer.writerow(row)
    #         f.close()

    # def displayTable(self):
    #     if not self.stats:
    #         print('no data loaded');
    #         return 

    #     columns = 0
    #     column_widths = []

    #     stats = self.stats;

    #     if self.keys():
    #         stats = [self.keys()] + self.stats

    #     for row in stats: 
    #         if len(row) > columns:
    #             columns = len(row)
    #         for index, data in enumerate(row):
    #             if len(column_widths) <= index:
    #                 column_widths.append(0)
    #             if column_widths[index] < len(str(data)):
    #                 column_widths[index] = len(str(data))

    #     row_format = ""
    #     row_length = 0
    #     for width in column_widths:
    #         row_format += "{:>" + str(width+3) +"}"
    #         row_length += width + 3

    #     for stat in stats:
    #         print("-" * row_length);
    #         print(row_format.format(*stat).strip())

    # def formatRow(self, stat):
        
    #     formatted_row = []
    #     for stat_item in self.keys():
    #         if not stat.get(stat_item): 
    #             formatted_row.append(0);
    #             continue
    #         formatted_row.append(stat.get(stat_item));

    #     return formatted_row