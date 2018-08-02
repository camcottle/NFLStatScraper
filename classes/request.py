import urllib.request
import re
from .element import Element
from bs4 import BeautifulSoup

class Request(object): 

    # Initialize Team
    def __init__(self, url):
        self.url     = url

        self.response = self.sendRequest().read();
        self.response_html = BeautifulSoup(str(self.response), 'html.parser');
        # self.processData();

    def sendRequest(self):
        return urllib.request.urlopen(self.url);
    
    # def processData(self):
    #     tags =[]; 
    #     index = 0
    #     text = str(self.response).strip()
    #     while(index < len(text)):
    #         # Look for opening tags
    #         result = re.search('(<[^/>]+>)', str(text[index:]))

    #         if not result:
    #             break

    #         tags.append(result.group(0))
    #         index += len(result.group(0))

    #         if re.search("</([^>]+)>", text[index:]).start() < re.search("(<[^/>]+>)", text[index:]).start():
    #             print("closing tag")
    #         else:
    #             print("opening tag")

    def processData(self): 
        depth = 0
        index = 0
        html  = str(self.response).strip()

        element = self.getElement(16)
        self.displayData(element, depth);

    def displayData(self, element, depth):
        print(element.string)
        if len(element.children):
            depth += 1
            for child in element.children:
                self.displayData(child, depth)

    def getElement(self, index):

        text    = str(self.response[index:]).strip()
        element = re.search('<([^/>]+)>', str(text[index:]))
        index += len(element.group(0))
        element = Element(element.group());
        # check to see if the element closes
        if re.search("</([^>]+)>", text[index:]).start() < re.search("<([^/>]+)>", text[index:]).start():
            end = re.search("</([^>]+)>", text[index:]).start()
            return element;
        else:
            data = self.getElement(re.search("<([^/>]+)>", text[index:]).start())
            element.addChildren(data);
            return element