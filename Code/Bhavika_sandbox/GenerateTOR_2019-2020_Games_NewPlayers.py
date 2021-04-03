#load libraries
import pandas as pd
import numpy as np
import time
import requests
import os
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import playbyplay, playbyplayv2

#Step 1: Load the file we want to change. We want our results to be in TOR_GameLogs_2019-20_Regular
#TOR_GameLogs_2019-20_Regular is copied from GameLog 2014-2020 with 2019-2020, Regular season and TOR filters


filename = r'D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_Regular.csv'
df_TOR_2019_2020 = pd.read_csv(filename)

print(df_TOR_2019_2020)

#Step 2: Load Player replacement info from TOR_PlayerReplacement.xlsx
#Sheet 1 "TOR" has TOR player which we will replace and Sheet 2 "Non-TOR" has the players with better performance

xlsx = pd.ExcelFile(r'D:\McMaster\DAT205\Capstone\Data\TOR_PlayerReplacement_V2.xlsx')
tor_players = pd.read_excel(xlsx, 'TOR')
non_tor_players = pd.read_excel(xlsx, 'Non-TOR')

print('Toronto under-performers')
print('----------------------------------------------------------')
print(tor_players.head())
print('Replacement players')
print('----------------------------------------------------------')
print(non_tor_players.head())

#Step 3: For each Toronto player, we replace the stats with the non-toronto player stats in the GameLog file
newPlayers = pd.DataFrame()
for index, row in tor_players.iterrows():
    playerData = df_TOR_2019_2020[df_TOR_2019_2020['PLAYER_ID'] == row['PLAYER_ID']]
    print(playerData.shape)
    #Step 4: Replace all columns present in the replcement file
    for column in tor_players:
        print(column)
        print(row[column])
        newPlayer = non_tor_players.iloc[index]
        print(newPlayer[column])
        playerData[column] = newPlayer[column]
        
    df_TOR_2019_2020.drop(df_TOR_2019_2020[df_TOR_2019_2020['PLAYER_ID'] == row['PLAYER_ID']].index, inplace=True)

    if index == 0:
        newPlayers = playerData            
    else:
        newPlayers = pd.concat([newPlayers, playerData],ignore_index=True)

#newPlayers.to_csv('D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_NewPlayerData.csv') 

df_TOR_2019_2020 = pd.concat([df_TOR_2019_2020, newPlayers],ignore_index=True)
df_TOR_2019_2020.to_csv('D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_With_NewPlayers_V2.csv') 
