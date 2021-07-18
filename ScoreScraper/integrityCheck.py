## for data integrity check, make sure all data are there, without duplication.
import random
import json
from numpy.lib.arraysetops import unique
import pandas as pd
import numpy as np
import requests

def missingData(scoreTable):
    checklist = []
    checklist = random.sample(range(1, 1000), 100)
    player_file = open(r'./JsonData/topPlayers.json')
    player_json = json.load(player_file)

    for i in range(1,1001):
        if scoreTable[i, 0] != i:
            print("Error at " + i + "th position. Mismatch with rank in CSV rank data")
            return False
    
    return True

def findDuplicate(scoreTable):
    pureScores = scoreTable[:, 1:]
    checkedScores = []
    checkedScores = set()
    if len(np.unique(pureScores, axis = 0)) == len(pureScores):
        print("No Duplicates in data.")
    
    else:
        uniqueList = []
        uniqueList = np.unique(pureScores, axis = 0, return_index=False)
        print("List of unique indexes are as follows.")
        print(uniqueList)

scores = pd.read_csv(r'./CsvData/Scores.csv', encoding='unicode_escape', error_bad_lines=False)
scoreTable = scores.values

if missingData(scoreTable):
    print("No missing data.")

findDuplicate(scoreTable)