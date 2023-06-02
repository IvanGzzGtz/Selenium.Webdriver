from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import re
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
from mysql.connector import Error

    

# Select the team you want to download the players info 
def select_team(team_index):
    options = Options()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)    
    website = 'https://www.nba.com/players'   
    driver.get(website)
    teams = driver.find_element(By.XPATH, '//Select[@name="TEAM_NAME"]')
    all_teams = Select(teams)
    all_teams.select_by_index(team_index)

    #Get players URL based on the selected team
    list_of_href = []
    for a in driver.find_elements(By.XPATH, '//td[@class="primary text RosterRow_primaryCol__1lto4"]/a'):
        attri = a.get_attribute('href')
        list_of_href.append(attri)


    #Get the players names based on the selected team
    player_name = driver.find_elements(By.XPATH, '//div[@class="RosterRow_playerName__G28lg"]')
    players_names = []
    for player in player_name:
        player = player.text
        res = re.sub(r'[^a-zA-Z]', ' ', player)
        players_names.append(res)

    #Get the playerID and the website for the stats of that player
    j = 0
    i = 0      
    for value in list_of_href:
        value = re.findall('\d+', value)
        website = 'https://www.nba.com/stats/player/{}/boxscores-traditional'.format(value[0])
        i += 1
        driver.get(website)
        time.sleep(5)


        #Get the columns headers for the dataframe 
        columns_headers = driver.find_elements(By.XPATH, "//tr[@class='Crom_headers__mzI_m']/th")
        headers = [columns_headers.text for columns_headers in columns_headers]
        #If there is no data to extract continue else get the data 
        if not bool(headers):
            j += 1
            continue
        else:
            #Extract all the table data from the website in a list called data 
            elements = driver.find_elements(By.XPATH, "//table[@class='Crom_table__p1iZz']/tbody/tr/td")
            data = [e.text for e in elements]

            # Make dataframe structure 
            index = 0
            max_size = 21
            my_dic = {}
            list_size = 0

            # Make dataframe structure
            # e is the index of the list data extracted from the table website
            # Create the the dictionarie which each index represents a row of the dataframe 
            for e in data:
                if index in my_dic:
                    my_dic[index].append(e)
                else:
                    my_dic[index] = [e]
                if list_size >= max_size:
                    index += 1
                    list_size = 0
                else:
                    list_size += 1
            

            # Create the dataframe with the columns headers and each key of the dictionarie my_dic is the index of the row 
            # df.loc[0] selects the index(row number) of the dataframe and assigns the same index of my_dic dictionarie to that row
            df = pd.DataFrame(columns = headers)
            for key in my_dic:
                df.loc[key] = my_dic[key]
            # Create the day, month and year columns from the MATCH UP columns
            df['day'] = df['MATCH UP'].str.strip().str[4:6]
            df['month'] = df['MATCH UP'].str.strip().str[:3]
            df['year'] = df['MATCH UP'].str.strip().str[8:13]

            # Function to return a value for a string
            def monthnum(month):
                if month == 'Jan':
                    return 1
                elif month == 'Feb':
                    return 2
                elif month == 'Mar':
                    return 3
                elif month == 'Apr':
                    return 4
                elif month == 'May':
                    return 5
                elif month == 'Oct':
                    return 10
                elif month == 'Nov':
                    return 11
                elif month == 'Dec':
                    return 12

            # For each month in a string value it assigns a number to that string and returns that number Jan = 1
            # Drop the month column
            df['monthnum'] = df['month'].apply(monthnum)
            df.drop(['month'], axis = 1 , inplace = True)

            my_list = list(df)
            my_list = my_list[3:]
            df[my_list] = df[my_list].apply(pd.to_numeric)
            df['date'] = pd.to_datetime(dict(year = df.year, month = df.monthnum, day = df.day))
            df['vs'] = df['MATCH UP'].str.strip().str[-3:]
            df['homeoraway'] = df['MATCH UP'].str.strip().str[-5:-4]
            df.drop(['day','year','monthnum','MATCH UP',"FGM","FGA","FG%","3P%","FTM","FTA","FT%","OREB","DREB","PF","+/-"],axis = 1,  inplace = True)
            print(df)
            ''' 
            df.to_csv('{}.csv'.format(players_names[j]))
            j += 1
            '''
    driver.close()




select_team(1)