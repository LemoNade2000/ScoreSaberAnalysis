## pick and categorize maps for further usage.

import BaseClasses
import json
import pandas as pd
import csv

table = pd.read_csv(r'./CsvData/RankedSongs.csv', encoding= 'unicode_escape') 
mapTable = table.values
topMapList = [] ## list of 50 maps with top pps
MapList0to1Star = [] ## list of 50 maps with 0-1 star acc
MapList1to2Star = [] ## list of 50 maps with 1-2 star acc
MapList2to3Star = [] ## list of 50 maps with 2-3 star acc
MapList3to4Star = [] ## list of 50 maps with 3-4 star acc
MapList4to5Star = [] ## list of 50 maps with 4-5 star acc

topScores = open("./CsvData/Scores.csv", 'w')
mapList = ["Rank"]

for ind in table.index:
    curMap = BaseClasses.map()
    curMap.diff = mapTable[ind, 2] # RankedSongs.csv column 2, Level(difficulty)
    curMap.hash = mapTable[ind, 16] # RankedSongs.csv column 16, ID(hash)

    if mapTable[ind, 6] >= 10:
        topMapList.append(curMap)
    elif mapTable[ind, 6] <= 1:
        MapList0to1Star.append(curMap)
    elif mapTable[ind, 6] <= 2:
        MapList1to2Star.append(curMap)
    elif mapTable[ind, 6] <= 3:
        MapList2to3Star.append(curMap)
    elif mapTable[ind, 6] <= 4:
        MapList3to4Star.append(curMap)     
    elif mapTable[ind, 6] <= 1:
        MapList4to5Star.append(curMap)
    
    mapList.append(curMap.hash + curMap.diff)

topMapDict = {}

for map in topMapList :
    if map.hash not in topMapDict:
        topMapDict[map.hash] = [map.diff]
    else:
        topMapDict[map.hash].append(map.diff)
    
with open('./JsonData/topMaps.json', 'w') as fp:
    json.dump(topMapDict, fp, indent=4)

MapDict0to1Stars = {}
for map in MapList0to1Star :
    if map.hash not in MapDict0to1Stars:
        MapDict0to1Stars[map.hash] = [map.diff]
    else:
        MapDict0to1Stars[map.hash].append(map.diff)
    
with open('./JsonData/Maps0to1Stars.json', 'w') as fp:
    json.dump(MapDict0to1Stars, fp, indent=4)


MapDict1to2Stars = {}
for map in MapList1to2Star :
    if map.hash not in MapDict1to2Stars:
        MapDict1to2Stars[map.hash] = [map.diff]
    else:
        MapDict1to2Stars[map.hash].append(map.diff)
    
with open('./JsonData/Maps1to2Stars.json', 'w') as fp:
    json.dump(MapDict1to2Stars, fp, indent= 4)

MapDict2to3Stars = {}
for map in MapList2to3Star :
    if map.hash not in MapDict2to3Stars:
        MapDict2to3Stars[map.hash] = [map.diff]
    else:
        MapDict2to3Stars[map.hash].append(map.diff)
    
with open('./JsonData/Maps2to3Stars.json', 'w') as fp:
    json.dump(MapDict2to3Stars, fp, indent= 4)

MapDict3to4Stars= {}
for map in MapList3to4Star :
    if map.hash not in MapDict3to4Stars:
        MapDict3to4Stars[map.hash] = [map.diff]
    else:
        MapDict3to4Stars[map.hash].append(map.diff)
    
with open('./JsonData/Maps3to4Stars.json', 'w') as fp:
    json.dump(MapDict3to4Stars, fp, indent= 4)

MapDict4to5Stars = {}
for map in MapList4to5Star :
    if map.hash not in MapDict4to5Stars:
        MapDict4to5Stars[map.hash] = [map.diff]
    else:
        MapDict4to5Stars[map.hash].append(map.diff)
    
with open('./JsonData/Maps4to5Stars.json', 'w') as fp:
    json.dump(MapDict4to5Stars, fp, indent= 4)

writer = csv.writer(topScores)
writer.writerow(mapList)

topScores.close()