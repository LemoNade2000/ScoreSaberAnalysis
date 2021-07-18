import pandas as pd
import numpy as np
import csv
from matplotlib import pyplot as plt

mapList = list(pd.read_csv("./CsvData/Scores.csv", nrows=1))

def twoMapCorr(hash1 = "21A989606D52EDF96B2971DBEDE366B1D0523088Expert", hash2 = "42C10857AF7E114C71A1B9F598E8462BA07C3DC1Expert+", boundaryScore = 0.85):
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
    r = np.corrcoef(firstMapScores, secondMapScores)
    print(str(r)) ## correlation matrix
    plt.scatter(firstMapScores, secondMapScores)
    plt.show()

twoMapCorr(boundaryScore = 0.85) ## default map x = Felis Expert, y = Donut Hole Expert+, with boundary being 0.85