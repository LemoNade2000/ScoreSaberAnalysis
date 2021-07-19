## base classes used

class map:
    def __init__(self):
        self.hash = ""
        self.diff = ""
        self.name = ""
        self.author = ""
        self.correlatedMaps = []
        self.star = 0
class mapScore:
    def __init__(self):
        self.map = map
        self.score = 0

class player:
    def __init__(self):
        self.playerID = 0
        self.playerRank = 0 
        self.mapScores = [] ## array of scores on a map that counts
        self.firstAcc = 0 ## 0~1 star Max Acc
        self.secondAcc = 0 ## 1~2 star Max Acc
        self.thirdAcc = 0 ## 2~3 star Max Acc
        self.fourthAcc = 0 ## 3~4 star Max Acc
        self.fifthAcc = 0 ## 4~5 star Max Acc