import numpy as np
import pandas as pd
import scipy as sp
import csv
import joblib
from sklearn.ensemble import RandomForestClassifier

useOriginalData = True

if(useOriginalData):
    #toronto_playerGamelogs = pd.read_csv('D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_Regular.csv')
    toronto_playerGamelogs = pd.read_csv('D:\McMaster\DAT205\Capstone\Data\AggrgatedTORGameLogs\DAT205_Output_Enhanced_df_TF_TOR.csv')
else:
    toronto_playerGamelogs = pd.read_csv('D:\McMaster\DAT205\Capstone\Data\TOR_GameLogs_2019-20_With_NewPlayers.csv')

print(toronto_playerGamelogs.shape)

toronto_playerGamelogs = toronto_playerGamelogs[toronto_playerGamelogs["TEAM_ABBREVIATION"] == "TOR"]


print(toronto_playerGamelogs.shape)

toronto_playerGamelogs = toronto_playerGamelogs[toronto_playerGamelogs["Game_Type"] == "Regular Season"]
print(toronto_playerGamelogs.shape)


selectedColumns = ['GAME_ID', 'GAME_DATE', 'MATCHUP', 'MIN', 'FGM', 'FGA',
       'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
       'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS',
       'PLUS_MINUS', 'DD2', 'TD3', 'PER']

#For replacement data, Drop WL
if(useOriginalData):
    selectedColumns.append("WL")

toronto_playerGamelogs = toronto_playerGamelogs[selectedColumns]
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

aggregateddata['TEAM_NAME'] = 'Toronto Raptors'
aggregateddata['TEAM_ABBREVIATION'] = 'TOR'
aggregateddata['TEAM_ID'] = '1610612761'
aggregateddata['SEASON_YEAR'] = '2019-20'
aggregateddata['Game_Type'] = 'Regular Season'


print(aggregateddata)

#save file
if(useOriginalData):
    aggregateddata.to_csv('D:\McMaster\DAT205\Capstone\Data\AggrgatedTORGameLogs\AggrgatedTORGameLogs_2014-2020_Regular.csv') 
else:
    aggregateddata.to_csv('D:\McMaster\DAT205\Capstone\Data\AggrgatedTORGameLogs\AggrgatedTORGameLogs_2019-2020_Regular_NewPlayers.csv') 



