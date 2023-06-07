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
    teams_select = driver.find_element(By.XPATH, '//Select[@name="TEAM_NAME"]')
    # Select the teams tag
    teams = driver.find_elements(By.TAG_NAME, 'Select')
    teams_names = teams[1]
    # Retrieve all the option (teams) elements within the select tag
    option_elements = teams_names.find_elements(By.TAG_NAME, 'option')
    
    # Extract the option values and store them in a list
    team_names = [option.get_attribute('value') for option in option_elements]

    # Assign the teams list to a varibale called team_names
    all_teams = Select(teams_select)
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

    players_names = [item.replace(" ", "_") for item in players_names]

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
            df['team'] = "{}".format(team_names[team_index])
            df['player'] = "{}".format(players_names[j])
            j += 1

            df.drop(['year','monthnum','MATCH UP',"FGM","FGA","FG%","3P%","FTM","FTA","FT%","OREB","DREB","PF","+/-"],axis = 1,  inplace = True)
                        # Connect to the MySQL server
            cnx = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="uzvi2ADTdSMA44Dn1Bcu"
                )
                # Create a new database if it doesn't exist
            database_name = "NBA"
            cursor = cnx.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
            cursor.close()

            # Switch to the newly created database
            cnx.database = database_name

            # Create a table and insert data from a DataFrame
            table_name = "{}".format(team_names[team_index])

            # Create the table
            create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (WL VARCHAR(1), MIN INT, PTS INT, 3PM INT, 3PA INT, REB INT, AST INT, STL INT, BLK INT, TOV INT, day INT, date DATE, vs VARCHAR(5), homeoraway VARCHAR(1), team VARCHAR(15), player VARCHAR(50))"
            cursor = cnx.cursor()
            try:
                cursor.execute(create_table_query)
            except Exception as e:
                # Handle the error
                print("An error occurred:", str(e))
                # Or you can choose to do nothing and simply pass
                pass
            cursor.close()

            # Insert the DataFrame data into the table
            insert_query = f"INSERT INTO `{table_name}` (WL, MIN, PTS, 3PM, 3PA, REB, AST, STL, BLK, TOV, day, date, vs, homeoraway, team, player) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = cnx.cursor()
            for _, row in df.iterrows():
                try:
                    cursor.execute(insert_query, (row["W/L"], row["MIN"], row["PTS"], row["3PM"], row["3PA"], row["REB"], row["AST"], row["STL"], row["BLK"], row["TOV"], row["day"], row["date"], row["vs"],  row["homeoraway"], row["team"],  row["player"]))
                except Exception as e:
                    print("An error occurred:", str(e))
                    pass            
            cursor.close()

            # Commit the changes and close the connection
            cnx.commit()
            cnx.close()



    driver.close()


i=1
for team in range(30):
    select_team(i)
    i+=1
    