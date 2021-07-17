## get top1000 people's score using api. Limited to 60 requests/min.

from typing import DefaultDict

import ratelimit
import base
import requests
import json
import sys
import pandas as pd
import csv
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=60, period=60)
def mapScores(playerRankStart, playerRankEnd):
    
    mapList = []
    mapList = list(pd.read_csv("Scores.csv", nrows=1))

    scores = open("Scores.csv", 'a', newline='')
    writer = csv.DictWriter(scores, fieldnames = mapList, extrasaction='ignore')

    jsonFile = open(r"topPlayers.json")
    playerDict = json.load(jsonFile)

    for rank in range(playerRankStart, playerRankEnd):
        i = 1
        dict = {}
        dict["Rank"] = str(rank)
        print("Loading " + str(rank) + "th player scores." )
        player = playerDict[str(rank)]
        while True:
            responseAPI = requests.get("https://new.scoresaber.com/api/player/" + player + "/scores/top/" + str(i))
            json_Data = responseAPI.json()
            if json_Data["scores"][0]["pp"] == 0:
                break ## no more ranked songs, break loop
            for j in range (0,8):
                if json_Data["scores"][j]["maxScore"] == 0:
                    break ## no more ranked songs, break loop
                songCode = ""
                songCode += json_Data["scores"][j]["songHash"]
                if json_Data["scores"][j]["difficultyRaw"] == "_ExpertPlus_SoloStandard":
                    songCode += "Expert+"
                elif json_Data["scores"][j]["difficultyRaw"] == "_Expert_SoloStandard":
                    songCode += "Expert"
                elif json_Data["scores"][j]["difficultyRaw"] == "_Hard_SoloStandard":
                    songCode += "Hard"
                elif json_Data["scores"][j]["difficultyRaw"] == "_Normal_SoloStandard":
                    songCode += "Normal"
                elif json_Data["scores"][j]["difficultyRaw"] == "_Easy_SoloStandard":
                    songCode += "Easy"  
                dict[songCode] = (json_Data["scores"][j]["score"]/json_Data["scores"][j]["maxScore"])
            i += 1 ## next page

        writer.writerow(dict)

    scores.close()

mapScores(1, 1000) ## put range of ranked players that you want to get scores of.