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

gameTypeListed = ['Regular Season', 'Playoffs']
# gameTypeListed = ['Pre Season', 'Regular Season', 'Playoffs']

# seasonsListed = ['2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10'
# , '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

seasonsListed = [ '2018-19','2019-20']
# Remove unwanted/useless attributes
unwanted_list = ['NBA_FANTASY_PTS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK'
, 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK'
, 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK'
, 'PTS_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 'TD3_RANK']


seasonStart = seasonsListed[0]
seasonEnd = seasonsListed[-1]
countFirstYear = 0

for seasonSelected in seasonsListed: 

    # For gameType in gameTypeListed:        
    for gameType in gameTypeListed:
        # Start counter for processing the current season
        start_time_counter_Season = time.time() 
        
        gamelogs_players = playergamelogs.PlayerGameLogs(season_nullable = seasonSelected, season_type_nullable = gameType)
        time.sleep(2) 
        df_gamelogs_players_currSeason = pd.DataFrame(gamelogs_players.get_data_frames()[0])
        df_gamelogs_players_currSeason.drop(unwanted_list, axis=1, inplace=True)
        print(df_gamelogs_players_currSeason)

        df_pgl_pbp = pd.DataFrame()
        for index, gamelog in df_gamelogs_players_currSeason.iterrows():
            print(gamelog['GAME_ID'])
            dfplaybyplay = pd.DataFrame(playbyplay.PlayByPlay(game_id = gamelog['GAME_ID'] ).get_data_frames()[0])     
            dfgamelog = df_gamelogs_players_currSeason.loc[df_gamelogs_players_currSeason['GAME_ID'] == gamelog['GAME_ID']]
            merged = pd.merge(dfgamelog, dfplaybyplay, how='inner', on= "GAME_ID")
            print(dfgamelog.shape)
            print(dfgamelog)
            print(dfplaybyplay.shape)
            print(merged.shape)       
            df_pgl_pbp = pd.concat([df_pgl_pbp, merged],ignore_index=(index>0))
            time.sleep(4) 

        #GAME_ID
        # Insert gameType column and list as one of the values in gameTypeListed
        df_gamelogs_players_currSeason['Game_Type'] = gameType
        if countFirstYear == 0:
            df_gamelogs_players = df_gamelogs_players_currSeason
            countFirstYear = 1
        else:
            # df_gamelogs_players = np.concatenate([df_gamelogs_players, df_gamelogs_players_currSeason])
            df_gamelogs_players = pd.concat([df_gamelogs_players, df_gamelogs_players_currSeason],ignore_index=True)
            # df_gamelogs_players = df_gamelogs_players.append(df_gamelogs_players_currSeason)

        time_took_Season = time.time() - start_time_counter_Season
        print("")
        print("Processed: Season =", seasonSelected, "| Game_Type =", gameType, "| ",  f"Process time: {hms_string(time_took_Season)}")
        # print(f"Process time: {hms_string(time_took_Season)}")
        time.sleep(2) 


# VALIDATION CODE 
if debug_active == 'yes':
    print(df_gamelogs_players)

#Save the data to the same folder that contains the notebook, example will be named 'Jamal Murray2019.csv'
# Setup file name for CSV
filename = 'HistoricalGameLogs_' + seasonStart + '_to_' + seasonEnd + '_ALL' + '.csv'
mergedfilename = 'pbg_pbp_' + seasonStart + '_to_' + seasonEnd + '_ALL' + '.csv'

df_gamelogs_players.to_csv(filename)
df_pgl_pbp.to_csv(mergedfilename)

time_took = time.time() - start_time
print("")
print("")
print("PROCESSING COMPLETE")
print(f"Total Runtime: {hms_string(time_took)}")