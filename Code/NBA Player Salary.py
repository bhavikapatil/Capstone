
import requests
from bs4 import BeautifulSoup
import numpy as np
#import BeautifulSoup4

import pandas as pd

data = {'Year':[],'Season_Year':[],'Rank': [],'Name': [],'Team': [],'Salary': []}
        
     #create dataframe
df_Salary = pd.DataFrame(data)

StartYear = 2021
#X = 2020

Year=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

for X in Year:
 if X == StartYear:
     URL = 'http://www.espn.com/nba/salaries'
 else:
     URL = 'http://www.espn.com/nba/salaries/_/year/'+ str(X)
 pg=requests.get(URL)
 soup = BeautifulSoup(pg.content, 'html.parser')
 res = soup.find_all(class_='page-numbers')
 pgnum = int(res[0].string[-2:])
 for i in range(1,pgnum):

     if (i > 1 and X == StartYear):
         URLcur = URL + '/_/page/' + str(i)
     #http://www.espn.com/nba/salaries/_/page/2
     elif i > 1:
         URLcur = URL + '/page/' + str(i)  
     else:
         URLcur = URL         
     print(URLcur)
     page=requests.get(URLcur)

     soup = BeautifulSoup(page.content, 'html.parser')
     results = soup.find(id='my-players-table')
     for test in results.find_all('tr', class_='oddrow'):
            Rank = test.find_all('td')[0].text
            Name = test.find_all('a')[0].text
            Salary = test.find_all('td')[3].text
            try: 
                Team= test.find_all('a')[1].text
            except:
                Team= test.find_all('td')[2].text
            new_row = {'Year':X,'Season Year': str(X-1)+"-"+str(X)[-2:] , 'Rank':Rank, 'Name':Name, 'Team':Team, 'Salary':Salary}
            df_Salary = df_Salary.append(new_row, ignore_index=True)
     for test in results.find_all('tr', class_='evenrow'):
            Rank = test.find_all('td')[0].text
            Name = test.find_all('a')[0].text
            Salary = test.find_all('td')[3].text
            try: 
                Team= test.find_all('a')[1].text
            except:
                Team= test.find_all('td')[2].text
            new_row = {'Year':X,'Season Year': str(X-1)+"-"+str(X)[-2:] , 'Rank':Rank, 'Name':Name, 'Team':Team, 'Salary':Salary}
            df_Salary = df_Salary.append(new_row, ignore_index=True)
 print (X) 

df_Salary['Rank']=df_Salary['Rank'].astype('int64')
df_Salary['Year']=df_Salary['Year'].astype('int64')
df_Salary_Sorted=df_Salary.sort_values(by=['Year', 'Rank'])     
#df_Salary_Sorted.to_csv('NBA Salary 2011-2021.csv', header=True)
df_Salary_Sorted.to_csv('NBA Salary 2011-2021.csv',
                        columns=['Year','Season Year','Rank','Name','Team','Salary'], 
                        index=False)


   