import pandas as pd
import numpy as np
import time
import requests
import os
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import playbyplay, playbyplayv2


filename = r'D:\McMaster\DAT205\Capstone\Data\TorontoPlayers_2014-2020.csv'
df_nonTOR_players = pd.read_csv(filename)


df_playerAverages = df_nonTOR_players.groupby(['PLAYER_NAME'], group_keys=False)[['PLUS_MINUS','PIE','PER', 'SALARY']].agg([np.mean])


df_playerAverages.reset_index(inplace=True)  


filetereddf = pd.DataFrame()
filetereddf['PLAYER_NAME'] = df_playerAverages['PLAYER_NAME'] 
filetereddf['PLUS_MINUS'] = df_playerAverages['PLUS_MINUS']
filetereddf['PIE'] = df_playerAverages['PIE']
filetereddf['PER'] = df_playerAverages['PER']
filetereddf['SALARY'] = df_playerAverages['SALARY']

filetereddf = filetereddf.loc[(filetereddf['PLUS_MINUS'] < 5.59) & (filetereddf['PIE'] < 9.37) &
(filetereddf['PER'] <15.99)].sort_values(["PLUS_MINUS", "PIE", "PER"]).head(5)

print("--------------------------------")
print(filetereddf)

print("--------------------------------")
print(filetereddf.shape)
