headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

import nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd 
import csv
import time




player_dict = players.get_players()
player_ids = []
print(len(player_dict))
    
playergamesDataframes = []

print(len(player_dict))
#1162, 1944, 2547 ids dont work
for i in range(2548, len(player_dict)):
    try:
        print(i)
        print(player_dict[i]['first_name'] + ' ' + player_dict[i]['last_name']) 
        playergames = playergamelog.PlayerGameLog(player_id=str(player_dict[i]['id']), season = SeasonAll.all).get_data_frames()
        df = pd.concat(playergames)
        df.to_csv('playergames_all_v.csv', mode='a', header=False)
        print(playergames)
        time.sleep(3) 
    except:
        continue
   
   # playergamesDataframes.append(playergames)
    #playergamesDataframes.to_csv('playergames2020.csv')

#playergamesDataframes.to_csv('playergames2020.csv')
#Call the API endpoint passing in lebron's ID & which season 
# gamelog_bron = playergamelog.PlayerGameLog(player_id='2544', season = '2018')

# #Converts gamelog object into a pandas dataframe
# #can also convert to JSON or dictionary  
# df_bron_games_2018 = gamelog_bron.get_data_frames()

#print(playergamesDataframes)
# If you want all seasons, you must import the SeasonAll parameter 
# from nba_api.stats.library.parameters import SeasonAll

# gamelog_bron_all = playergamelog.PlayerGameLog(player_id='2544', season = SeasonAll.all)

# df_bron_games_all = gamelog_bron_all.get_data_frames()
# print(df_bron_games_all)


# import pandas as pd
# from nba_api.stats.endpoints import synergyplaytypes
# iso = synergyplaytypes.SynergyPlayTypes(league_id = '00', per_mode_simple = 'Totals',
#                                        player_or_team_abbreviation = 'P', season_type_all_star = 'Regular Season',
#                                        type_grouping_nullable = 'Offensive', play_type_nullable = 'Isolation')
# iso.synergy_play_type.get_data_frame()
# print(iso.synergy_play_type.get_data_frame())