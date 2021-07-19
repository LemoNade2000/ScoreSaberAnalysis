import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import BaseClasses
import pandas as pd
import numpy as np
from scipy import stats
import csv
from matplotlib import pyplot as plt
import json


mapList = list(pd.read_csv("./CsvData/Scores.csv", nrows=1))

def twoMapCorr(hash1 = "21A989606D52EDF96B2971DBEDE366B1D0523088Expert", hash2 = "42C10857AF7E114C71A1B9F598E8462BA07C3DC1Expert+", boundaryScore = 0.8):
    mapList = list(pd.read_csv("./CsvData/Scores.csv", nrows=1))
    scores = pd.read_csv(r'./CsvData/Scores.csv', encoding='unicode_escape', error_bad_lines=False)
    scores = scores.fillna(0)
    scoresTable = scores.values
    firstIndex = mapList.index(hash1)
    secondIndex = mapList.index(hash2)
    mapScores = scoresTable[:, [firstIndex, secondIndex]]
    zeroIndex = []
    for i in range(1001):
        if mapScores[i][0] <= boundaryScore or mapScores[i][1] <= boundaryScore : ## arbitrary boundary for what one may consider "cleared"
            zeroIndex.append(i)
    mapScores = np.delete(mapScores, zeroIndex, axis = 0)
    firstMapScores = mapScores[:, 0]
    secondMapScores = mapScores[:, 1]
    r = stats.pearsonr(firstMapScores,secondMapScores)
    print(str(r)) ## correlation matrix
    return (r[0], len(mapScores))

def ppMapCorr(hash1 = "21A989606D52EDF96B2971DBEDE366B1D0523088Expert", boundaryScore = 0.8):
    mapList = list(pd.read_csv("./CsvData/Scores.csv", nrows=1))
    scores = pd.read_csv(r'./CsvData/Scores.csv', encoding='unicode_escape', error_bad_lines=False)
    scores = scores.fillna(0)
    scoresTable = scores.values
    firstIndex = mapList.index(hash1)
    secondIndex = mapList.index("PP")
    mapScores = scoresTable[:, [firstIndex, secondIndex]]
    zeroIndex = []
    for i in range(1001):
        if mapScores[i][0] <= boundaryScore:
            zeroIndex.append(i)
    mapScores = np.delete(mapScores, zeroIndex, axis = 0)
    firstMapScores = mapScores[:, 0]
    pps = mapScores[:, 1]
    r = stats.pearsonr(firstMapScores, pps)
    print(str(r)) ## correlation matrix
    return (r[0], len(mapScores))

def fisherZdiff(r1, r2, n1, n2, boundary):
    z1 = 0.5 * (np.log((1+r1)/(1-r1))) ## z1 = .5*ln((1+r1)/(1-r1)).
    z2 = 0.5 * (np.log((1+r2)/(1-r2)))
    sezdiff = np.sqrt((1/(n1-3)) + (1/(n2-3))) ##sezdiff = sqrt(1/(n1 - 3) + 1/(n2-3)).
    ztest = (z2 - z1)/sezdiff
    probability = 1 - stats.norm.cdf(ztest)
    print("z-value = " + str(ztest) + "\nProbability = " + str(probability))
    if probability > boundary:
        return (True, ztest) ## fail to reject null hypothesis
    else: return (False, ztest) ## reject null hypothesis

    # H0 = r2 = r1
    # Ha = r2 > r1
    # reject null hypothesis, if cdf(ztest) is significant. That is, if cdf(ztest) > 0.9, reject null hypothesis. Fail to reject if 1 - cdf > 0.1.
    # if 1 - cdf is greater than 0.1, than there is no significant evidence to reject null hypothesis, 
    # which means we can't say that the correlation between two maps is significantly larger than correlation between pp and the map.

def corrMaps(hash1):
    mapList = list(pd.read_csv("./CsvData/Scores.csv", nrows=1))
    mapList.remove("PP")
    mapList.remove("Rank")
    mapList.remove(hash1)
    correlatedMaps = []
    firstTest = ppMapCorr(hash1)
    (r1, n1) = firstTest
    table = pd.read_csv(r'./CsvData/RankedSongs.csv', encoding= 'unicode_escape') 
    mapTable = table.values
    currMap = BaseClasses.map()
    currMap.hash = hash1[:40]
    currMap.diff = hash1[40:]
    mapIndex = 0
    for i in range(len(mapTable)):
        if mapTable[i][2] == currMap.diff and mapTable[i][16] == currMap.hash:
            mapIndex = i
            break
    currMap.name = mapTable[mapIndex][0]
    currMap.author = mapTable[mapIndex][1]
    currMap.star = mapTable[mapIndex][6]
    farMaps = []
    for maps in mapTable:
        if np.abs(currMap.star - maps[6]) > 4:
            hash = ""
            hash += maps[16]
            hash += maps[2]
            print("removing" + hash)
            mapList.remove(hash)
    i = 1
    for maps in mapList:
        try: secondTest = twoMapCorr(hash1, maps)
        except: continue
        (r2, n2) = secondTest
        result = fisherZdiff(r1, r2, n1, n2, 0.1)
        if (result[0]) == False:
            tuple = (maps, result[1])
            correlatedMaps.append(tuple)
        i += 1
        print(str(i) + " / " + str(len(mapList)) + "\n Map : " + maps)
    
    correlatedMaps = sorted(correlatedMaps, key= lambda x : x[1], reverse= True)
    currMap.correlatedMaps = correlatedMaps
    path = './JsonData/CorrMaps/' + hash1 + '.json'
    with open(path, 'w') as fp:
        json.dump(currMap.__dict__, fp, indent=4)

corrMaps("F4DA02BFEC50EFDE4F2A1E4B89251E654B9C7353Expert+")

# hash1 = "558FD3C73D5F7E5BBBF1616760E099EBCFD75903Expert+"
# hash2 = "F4DA02BFEC50EFDE4F2A1E4B89251E654B9C7353Expert+"

# firstTest = ppMapCorr(hash1, boundaryScore=1.7)
# secondTest = twoMapCorr(hash1, hash2, boundaryScore = 0.7) ## default map x = Felis Expert, y = Donut Hole Expert+, with boundary being 0.85
# (r1, n1) = firstTest
# (r2, n2) = secondTest
# if(fisherZdiff(r1, r2, n1, n2, 0.1)[0]):
#     print("There is no significant evidence to reject the hypothesis that the correlation between two maps is same as the correlation between the map and PP.")
# else: print("There is enough statistical evidence to reject the hypothesis that the correlation between the two maps and the correlation between the map and PP is the same")

