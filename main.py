import requests
import json
import sys


class player:
    def __init__(self):
        self.playerID = 0
        self.playerRank = 0 

playerList = []
## get 20 pages of userIDs along with ranks. ##
for i in range (1, 21):
    responseAPI = requests.get('https://new.scoresaber.com/api/players/' +  str(i))
    json_data = responseAPI.json()
    for i in range (50):
        curPlayer = player()
        curPlayer.playerID = json_data['players'][i]['playerId']
        curPlayer.playerRank = json_data['players'][i]['rank']
        playerList.append(curPlayer)
sys.stdout = open('output.txt','w')
for i in range (1000):
    print("ID" + str(playerList[i].playerID) + "RANK" + str(playerList[i].playerRank) + "\n")

sys.stdout.close()
