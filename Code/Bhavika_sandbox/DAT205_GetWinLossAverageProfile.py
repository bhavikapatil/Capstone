import pandas as pd
import numpy as np
import time
import requests
import os
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import playbyplay, playbyplayv2

def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60))/60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h,m,s)

start_time = time.time()

filename = 'D:\McMaster\DAT205\Capstone\Data\HistoricalGameLogs_2004-05_to_2019-20_ALL.csv'
df_playergamelogs = pd.read_csv(filename)
unwanted_list = ['Unnamed: 0']

df_playergamelogs.drop(unwanted_list, axis=1, inplace=True)
print("PlayerGameLogs Shape: " + str(df_playergamelogs.shape))

uniqueGameIds = df_playergamelogs["GAME_ID"].astype(str).unique()
print("Number of total games: " + str(uniqueGameIds.shape))

print(df_playergamelogs.head())

print(df_playergamelogs["WL"].unique())
w = df_playergamelogs['WL'] != 'W'
df_WinGameLogs, df_LossGamelogs = df_playergamelogs[w], df_playergamelogs[~w]

print("WinGameLogs Shape: " + str(df_WinGameLogs.shape))
print("LossGameLogs Shape: " + str(df_LossGamelogs.shape))

performanceColumns= ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
       'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK',
       'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'DD2', 'TD3']

df_WinGameLogsmean = pd.DataFrame(df_WinGameLogs[performanceColumns].mean(axis = 0)).transpose()
df_WinGameLogsmean["WinLoss"] = "W"
df_WinGameLogsmean["Team"] = "ALL"

print("df_WinGameLogsmean")
print(df_WinGameLogsmean)

df_LossGamelogsmean = pd.DataFrame(df_LossGamelogs[performanceColumns].mean(axis = 0)).transpose()
df_LossGamelogsmean["WinLoss"] = "L"
df_LossGamelogsmean["Team"] = "ALL"

print("df_LossGamelogsmean")
print(df_LossGamelogsmean)

df_TOR_WinGameLogs = df_WinGameLogs[df_WinGameLogs['TEAM_ABBREVIATION']=='TOR']
df_TOR_WinGameLogsmean = pd.DataFrame(df_TOR_WinGameLogs[performanceColumns].mean(axis = 0)).transpose()
df_TOR_WinGameLogsmean["WinLoss"] = "W"
df_TOR_WinGameLogsmean["Team"] = "TOR"

print("df_TOR_WinGameLogsmean")
print(df_TOR_WinGameLogsmean)

df_TOR_LossGamelogs = df_LossGamelogs[df_LossGamelogs['TEAM_ABBREVIATION']=='TOR']
df_TOR_LossGamelogsmean = pd.DataFrame(df_TOR_LossGamelogs[performanceColumns].mean(axis = 0)).transpose()
df_TOR_LossGamelogsmean["WinLoss"] = "L"
df_TOR_LossGamelogsmean["Team"] = "TOR"

print("df_TOR_LossGamelogsmean")
print(df_TOR_LossGamelogsmean)

df_mean = df_WinGameLogsmean
df_mean = df_mean.append(df_LossGamelogsmean) 
df_mean = df_mean.append(df_TOR_WinGameLogsmean) 
df_mean = df_mean.append(df_TOR_LossGamelogsmean) 

meanfilename = 'D:\McMaster\DAT205\Capstone\Data\statsMean.csv'
pd.DataFrame(df_mean).to_csv(meanfilename)

time_took = time.time() - start_time
print("")
print("")
print("PROCESSING COMPLETE")
print(f"Total Runtime: {hms_string(time_took)}")
