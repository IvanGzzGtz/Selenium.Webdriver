from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd 
from get_tables import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import re


def team(index):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(PATH, options=options)
    website = 'https://www.nba.com/players'   
    driver.get(website)
    x = driver.find_element(By.XPATH, '//Select[@name="TEAM_NAME"]')
    drop = Select(x)
    # Select by index 
    drop.select_by_index(index)

    list_of_href = []

    for a in driver.find_elements(By.XPATH, '//td[@class="primary text RosterRow_primaryCol__1lto4"]/a'):
        attri = a.get_attribute('href')
        list_of_href.append(attri)
    
    

    player_name = driver.find_elements(By.XPATH, '//div[@class="RosterRow_playerName__G28lg"]')
    players_names = []
    for player in player_name:
        player = player.text
        res = re.sub(r'[^a-zA-Z]', '', player)
        players_names.append(res)


    j = 0
    i = 0      
    for value in list_of_href:
        value = re.findall('\d+', value)
        website = 'https://www.nba.com/stats/player/{}/boxscores-traditional'.format(value[0])
        i += 1
        # driver.close()
        driver.get(website)
        time.sleep(5)
        matches = driver.find_elements(By.XPATH, "//tr[@class='Crom_headers__mzI_m']/th")
        headers = [match.text for match in matches]
        if not bool(headers):
            j += 1
            continue
        else:
            elements = driver.find_elements(By.XPATH, "//table[@class='Crom_table__p1iZz']/tbody/tr/td")
            data = [e.text for e in elements]

            index = 0
            max_size = 21
            my_dic = {}
            list_size = 0

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
            
            df = pd.DataFrame(columns = headers)
            for key in my_dic:
                df.loc[key] = my_dic[key]
            
            df['day'] = df['MATCH UP'].str.strip().str[4:6]
            df['month'] = df['MATCH UP'].str.strip().str[:3]
            df['year'] = df['MATCH UP'].str.strip().str[8:13]

            def monthnum(month):
                if month == 'Jan':
                    return 1
                elif month == 'Feb':
                    return 2
                elif month == 'Mar':
                    return 3
                elif month == 'Apr':
                    return 4
                elif month == 'Oct':
                    return 10
                elif month == 'Nov':
                    return 11
                elif month == 'Dec':
                    return 12

            df['monthnum'] = df['month'].apply(monthnum)
            df.drop(['month'], axis = 1 , inplace = True)

            my_list = list(df)
            my_list = my_list[3:]
            df[my_list] = df[my_list].apply(pd.to_numeric)
            df['date'] = pd.to_datetime(dict(year = df.year, month = df.monthnum, day = df.day))
            df['vs'] = df['MATCH UP'].str.strip().str[-3:]
            df['homeoraway'] = df['MATCH UP'].str.strip().str[-5:-4]
            df.drop(['day','year','monthnum','MATCH UP',"W/L","MIN","FGM","FGA","FG%","3PA","3P%","FTM","FTA","FT%","OREB","DREB","PF","+/-"],axis = 1,  inplace = True)
            df.to_csv('{}.csv'.format(players_names[j]))
            j += 1
    driver.close()
team(1)
time.sleep(2)
team(2)
time.sleep(2)
team(3)
team(4)
team(5)
team(6)
team(7)
team(8)
team(9)
team(10)
team(11)
team(12)
team(13)
team(14)
team(15)
team(16)
team(17)
team(18)
team(19)
team(20)
team(21)
team(22)
team(23)
team(24)
team(25)
team(26)
team(27)
team(28)
team(29)
team(30)



"""    """