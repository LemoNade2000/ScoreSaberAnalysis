## get top1000 people's score using api. Limited to 60 requests/min.
from typing import DefaultDict

import requests
import json
import pandas as pd
import csv
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=60, period=60)
def mapScores(playerRankStart, playerRankEnd):
    
    mapList = []
    mapList = list(pd.read_csv("./CsvData/Scores.csv", nrows=1))

    scores = open("./CsvData/Scores.csv", 'a', newline='')
    writer = csv.DictWriter(scores, fieldnames = mapList, extrasaction='ignore')

    jsonFile = open(r"./JsonData/topPlayers.json")
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

def getPP():

    df = pd.read_csv(r"./CsvData/Scores.csv")
    df["PP"] = 0

    jsonFile = open(r"./JsonData/topPlayers.json")
    playerDict = json.load(jsonFile)

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    cols = df.columns.tolist()
    newcols = cols[:0] + cols[-1:] + cols[1:-1]
    df = df[newcols]
    dt = df.values

    ppIndex = newcols.index("PP")
    for i in range (1,1001):
        player = playerDict[str(i)]
        responseAPI = requests.get("https://new.scoresaber.com/api/player/" + player + "/basic")
        json_Data = responseAPI.json()
        dt[i][ppIndex] = json_Data["playerInfo"]["pp"]
    
    df = pd.DataFrame(dt, columns = newcols)
    df.to_csv(r"./CsvData/Scores.csv")


mapScores(1, 1001) ## put range of ranked players that you want to get scores of.
getPP()