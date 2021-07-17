## stores top1000 users into json file.

import base
import requests
import json
import sys
import pandas

playerList = []
## get 20 pages of userIDs along with ranks.
for i in range (1, 21):
    responseAPI = requests.get('https://new.scoresaber.com/api/players/' +  str(i))
    json_data = responseAPI.json()
    for i in range (50):
        curPlayer = base.player()
        curPlayer.playerID = json_data['players'][i]['playerId']
        curPlayer.playerRank = json_data['players'][i]['rank']
        playerList.append(curPlayer)

playersDict = {}

for i in range (len(playerList)):
    playersDict[playerList[i].playerRank] = playerList[i].playerID

with open('topPlayers.json', 'w') as fp:
    json.dump(playersDict, fp, indent= 4)