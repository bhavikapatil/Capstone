import pandas as pd
import numpy as np
import time
import requests
import os


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60))/60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h,m,s)

start_time = time.time()

filename = 'D:\McMaster\DAT205\Capstone\Data\PlaybyPlay_ALL.csv'
df_playbyplay = pd.read_csv(filename)

print(df_playbyplay.head())
print(df_playbyplay.columns)


time_took = time.time() - start_time
print("")
print("")
print("PROCESSING COMPLETE")
print(f"Total Runtime: {hms_string(time_took)}")
