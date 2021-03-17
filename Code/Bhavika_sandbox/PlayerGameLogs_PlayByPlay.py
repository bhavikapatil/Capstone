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
debug_active = 'yes'

filename = 'D:\McMaster\DAT205\Capstone\Code\HistoricalGameLogs_2004-05_to_2019-20_ALL.csv'
df_playergamelogs = pd.read_csv(filename)
unwanted_list = ['Unnamed: 0']

df_playergamelogs.drop(unwanted_list, axis=1, inplace=True)
print("PlayerGameLogs Shape: " + str(df_playergamelogs.shape))

uniqueGameIds = df_playergamelogs["GAME_ID"].astype(str).unique()
print("Number of games: " + str(uniqueGameIds.shape))

df_playbyplay = pd.DataFrame()
failedGameIds = np.array([])
index = 0
for game_id in uniqueGameIds:
    game_id = "00" + game_id
    print(game_id)
    try:
        df_game_playbyplay = pd.DataFrame(playbyplay.PlayByPlay(game_id =  game_id).get_data_frames()[0])
        df_playbyplay = pd.concat([df_playbyplay, df_game_playbyplay],ignore_index=(index > 0))
        print("Index: " + str(index))
        index = index + 1
        time_took_Season = time.time() - start_time
        print("")
        print("Processed: Game ID =", game_id,  f"Process time: {hms_string(time_took_Season)}")
        # print(f"Process time: {hms_string(time_took_Season)}")
        time.sleep(2) 
    except:
        print("Error Processing: Game ID =", game_id)
        failedGameIds =  np.append(failedGameIds, game_id)


playbyplayfilename = 'D:\McMaster\DAT205\Capstone\Code\PlaybyPlay_ALL.csv'

df_playbyplay.to_csv(playbyplayfilename)

time_took = time.time() - start_time
print("")
print("")
print("PROCESSING COMPLETE")
print(f"Total Runtime: {hms_string(time_took)}")
print(f"Total Failed GameIds: {failedGameIds.shape}")
print("--------------Failed Game Ids--------------")
print(failedGameIds)