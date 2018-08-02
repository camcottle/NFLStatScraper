class Element(object): 

    # Initialize Team
    def __init__(self, string):
        self.string   = string
        self.children = []

    def addChildren(self, child):
        self.children.append(child)