from urllib import request, parse
import csv
import json

stats = [
    'defensive',
    'fumbles',
    'interceptions',
    'kicking',
    'passing',
    'punting',
    'receiving',
    'rushing'
]

for stat in stats: 

    with open(stat + '.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 

            game_id   = row['game_id']
            player_id = row['player_id']
            
            del row['game_id']
            del row['home']
            del row['player_id']

            stat_data = {
                "game": int(game_id),
                "player": int(player_id),
                "type": stat,
                "stats": row
            }

            data = json.dumps(stat_data).encode('utf-8')
            req = request.Request('http://localhost:3003/v1/stats/import/', data=data, method='POST', headers={'Content-Type': "application/json"})
            res = request.urlopen(req).read()
    csvfile.close()
