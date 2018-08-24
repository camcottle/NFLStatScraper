import urllib.request
import http
from bs4 import BeautifulSoup
import re
import time

class PlayerScraper(object):

    def __init__(self, player_id):
        self.player_id   = player_id

        self.data = {
            "id": player_id,
            "dob": None,
            "number": None,
            "college": None,
            "position": None,
            "draft_year": None,
            "draft_pick": None,
            "draft_round": None,
        }

    def scrape(self):
        html = self.sendRequest()
        document = BeautifulSoup(html.decode('utf-8'), 'lxml')
        self.data["name"] = document.h1.get_text()
        bio = document.find('div', class_="player-bio")


        player_meta = bio.find_all('ul')
        
        for data in player_meta[0].find_all("li"):
            if re.search('\#(\d)+ (\w{2})', data.get_text()):
                number_pos = re.search('\#(\d)+ (\w{2})', data.get_text())
                self.data['number']   = number_pos.group(1)
                self.data['position'] = number_pos.group(2)


        for data in player_meta[1].find_all("li"):
            if "Born" in data.get_text():
                self.setBirthday(data.get_text())
            if "Drafted" in data.get_text():
                self.setDraft(data.get_text())
            if "College" in data.get_text():
                self.setCollege(data.get_text())


        return self.data

    def setBirthday(self, string):
        self.data['dob'] = re.search('[a-zA-Z]+ [0-9]{1,2}, [0-9]{4}', string.replace('Born', '')).group(0)

    def setCollege(self, string):
        self.data['college'] = string.replace('College', '')

    def setDraft(self, string):
        string = string.replace('Drafted ', '')
        query = re.search('([0-9]{4}): (\d+)[a-z]{2} Rnd, (\d{1,3})[a-z]{2}', string)
        self.data['draft_year']  = query.group(1)
        self.data['draft_round'] = query.group(2)
        self.data['draft_pick']  = query.group(3)

    def sendRequest(self):
        path = "http://www.espn.com/nfl/player/stats/_/id/{}/"
        
        try:
            page = urllib.request.urlopen(path.format(self.player_id)).read();
        except (http.client.IncompleteRead, HTTPError) as e:
            print("unable to read, trying again")
            time.sleep(10)
            page = urllib.request.urlopen(path.format(self.player_id)).read();
        return page