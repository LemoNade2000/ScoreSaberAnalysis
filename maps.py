## pick and categorize maps for further usage.

import base
import requests
import json
import sys
import pandas as pd
import numpy as np
import csv

table = pd.read_csv (r'RankedSongs.csv', encoding= 'unicode_escape')
mapTable = table.values
topMapList = [] ## list of 50 maps with top pps
firstAccList = [] ## list of maps with 0~1 star range, and so on
secondAccList = [] 
thirdAccList = []
fourthAccList = []
fifthAccList = []

topScores = open("Scores.csv", 'w')
mapList= []
mapList.append("Rank")

for ind in table.index:
    curMap = base.map()
    curMap.diff = mapTable[ind, 2]
    curMap.hash = mapTable[ind, 16]

    if mapTable[ind, 6] >= 10:
        topMapList.append(curMap)

    elif mapTable[ind, 6] <= 1:
        firstAccList.append(curMap)

    elif mapTable[ind, 6] <= 2:
        secondAccList.append(curMap)

    elif mapTable[ind, 6] <= 3:
        thirdAccList.append(curMap)

    elif mapTable[ind, 6] <= 4:
        fourthAccList.append(curMap)
        
    elif mapTable[ind, 6] <= 1:
        fifthAccList.append(curMap)
    
    mapList.append(curMap.hash + curMap.diff)

topMapDict = {}

for map in topMapList :
    if map.hash not in topMapDict:
        topMapDict[map.hash] = [map.diff]
    else:
        topMapDict[map.hash].append(map.diff)
    
with open('topMaps.json', 'w') as fp:
    json.dump(topMapDict, fp, indent= 4)

firstAccDict = {}
for map in firstAccList :
    if map.hash not in firstAccDict:
        firstAccDict[map.hash] = [map.diff]
    else:
        firstAccDict[map.hash].append(map.diff)
    
with open('firstAccMaps.json', 'w') as fp:
    json.dump(firstAccDict, fp, indent= 4)


secondAccDict = {}
for map in secondAccList :
    if map.hash not in secondAccDict:
        secondAccDict[map.hash] = [map.diff]
    
    else:
        secondAccDict[map.hash].append(map.diff)
    
with open('secondAccMaps.json', 'w') as fp:
    json.dump(secondAccDict, fp, indent= 4)

thirdAccDict= {}
for map in thirdAccList :
    if map.hash not in thirdAccDict:
        thirdAccDict[map.hash] = [map.diff]
    
    else:
        thirdAccDict[map.hash].append(map.diff)
    
with open('thirdAccMaps.json', 'w') as fp:
    json.dump(thirdAccDict, fp, indent= 4)

fourthAccDict= {}
for map in fourthAccList :
    if map.hash not in fourthAccDict:
        fourthAccDict[map.hash] = [map.diff]
    
    else:
        fourthAccDict[map.hash].append(map.diff)
    
with open('fourthAccMaps.json', 'w') as fp:
    json.dump(fourthAccDict, fp, indent= 4)

fifthAccDict = {}
for map in fifthAccList :
    if map.hash not in fifthAccDict:
        fifthAccDict[map.hash] = [map.diff]
    
    else:
        fifthAccDict[map.hash].append(map.diff)
    
with open('fifthAccMaps.json', 'w') as fp:
    json.dump(fifthAccDict, fp, indent= 4)

writer = csv.writer(topScores)
writer.writerow(mapList)

topScores.close()