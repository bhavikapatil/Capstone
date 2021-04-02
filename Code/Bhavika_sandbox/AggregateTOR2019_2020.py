import numpy as np
import pandas as pd
import scipy as sp
import csv
import joblib
from sklearn.ensemble import RandomForestClassifier

useOriginalData = False

if(useOriginalData):
    toronto_playerGamelogs = pd.read_csv('D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_Regular.csv')
else:
    toronto_playerGamelogs = pd.read_csv('D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_With_NewPlayers.csv')

dropColumns = ['SEASON_YEAR', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID',
       'TEAM_ABBREVIATION', 'TEAM_NAME', 'PIE', 'SALARY', 'Game_Type', 'UID_STG']

#For replacement data, Drop WL
if(not useOriginalData):
    dropColumns.append("WL")

toronto_playerGamelogs = toronto_playerGamelogs.drop(dropColumns, axis = 1)

print(toronto_playerGamelogs.columns)

#For original TOR data, keep WL, for replacedments, remove it
if(useOriginalData):
    aggregateddata = toronto_playerGamelogs.groupby(['GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL']).sum()
else:
    aggregateddata = toronto_playerGamelogs.groupby(['GAME_ID', 'GAME_DATE', 'MATCHUP']).sum()

aggregateddata = aggregateddata.reset_index()

aggregateddata['FG_PCT'] = aggregateddata['FGM'] / aggregateddata['FGA']
aggregateddata['FG3_PCT'] = aggregateddata['FG3M'] / aggregateddata['FG3A']
aggregateddata['FT_PCT'] = aggregateddata['FTM'] / aggregateddata['FTA']

print(aggregateddata)

#save file
if(useOriginalData):
    aggregateddata.to_csv('D:\McMaster\DAT205\Capstone\Data\AggrgatedTORGameLogs\AggrgatedTORGameLogs_2019-2020_Regular.csv') 
else:
    aggregateddata.to_csv('D:\McMaster\DAT205\Capstone\Data\AggrgatedTORGameLogs\AggrgatedTORGameLogs_2019-2020_Regular_NewPlayers.csv') 



