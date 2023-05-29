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

class Get_info():
    def team(team):
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
        drop.select_by_index(team)
        
        list_of_href = []
        list_of_ids = []
        for a in driver.find_elements(By.XPATH, '//td[@class="primary text RosterRow_primaryCol__1lto4"]/a'):
                attri = a.get_attribute('href')
                list_of_href.append(attri)
                pattern="\d+"
                str_list=re.findall(pattern,attri)
                list_of_ids.append(str_list)
                



        for value in list_of_href:
            website = value 
            driver.get(website)
            stats_element = driver.find_elements(By.LINK_TEXT , 'Stats')
            stats_element[1].click()
            get_url = driver.current_url
            website = get_url + '/boxscores-traditional'
            driver.get(website)
            time.sleep(100)



        

        

Get_info.team(1)