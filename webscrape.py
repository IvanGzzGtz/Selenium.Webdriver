from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd 
import time
from get_tables import *




#Here starts the function get_csv() 
def get_csv(player, url):

    # We call the path and set the settings for the webdriver. 
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(PATH, options=options)


    #We call the url of the function website and get that website
    website = url
    driver.get(website)
    click = driver.find_elements(By.XPATH, '//select[@name='TEAM_NAME']/option')




    select_list = []
    for value in click:
        a = value.text
        select_list.append(a)
    
    

    i = 0
    for value in select_list:
        if i ==0:
            actual_year = get_tables(value, url)
            i += 1
        else:
            pass
            
            """past_year = get_tables(value, url)
        driver.quit()
    table = actual_year.append(past_year)
    table.reset_index(inplace = True)"""

    table['day'] = table['MATCH UP'].str.strip().str[4:6]
    table['month'] = table['MATCH UP'].str.strip().str[:3]
    table['year'] = table['MATCH UP'].str.strip().str[8:13]

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

    table['monthnum'] = table['month'].apply(monthnum)
    table.drop(['month'], axis = 1 , inplace = True)

    my_list = list(table)
    my_list = my_list[3:]
    table[my_list] = table[my_list].apply(pd.to_numeric)
    table['date'] = pd.to_datetime(dict(year = table.year, month = table.monthnum, day = table.day))
    table['vs'] = table['MATCH UP'].str.strip().str[-3:]
    table['homeoraway'] = table['MATCH UP'].str.strip().str[-5:-4]
    table.drop(['day','year','monthnum','MATCH UP', 'index'],axis = 1,  inplace = True)
    table.to_csv('{}.csv'.format(player))




    """ 
    def get_csv(player, url):
        path = 'User'

    """

