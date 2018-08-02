import urllib.request

class Scraper(object): 

    # Initialize Team
    def __init__(self, props):
        self.host     = props["host"]
        self.protocol = props["protocol"]
        self.path     = props["path"]

        self.response = self.sendRequest().read()

    def getURL(self):
        return (self.protocol + "://" + self.host + "/" + self.path);

    def sendRequest(self):
        url = self.getURL()
        return urllib.request.urlopen(url);
    