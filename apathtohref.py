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


 # We call the path and set the settings for the webdriver. 
PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH, options=options)
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
#We call the url of the function website and get that website
website = 'https://www.nba.com/players'   
driver.get(website)
cursor = driver.find_elements(By.XPATH, '//Select[@name="TEAM_NAME"]/option')
for value in cursor:
    value.click()
    time.sleep(10)
    
    for a in driver.find_elements(By.XPATH, '//td[@class="primary text RosterRow_primaryCol__1lto4"]/a'):
        attri = a.get_attribute('href')
        print(attri)
        time.sleep(2)
'''
list_of_teams = []
i = 0
for value in cursor:
    drop.select_by_index(i)
    i = i+1
     '''


'''
click = driver.find_elements(By.XPATH, '//Table[@class="players-list"]/tbody')
    click = driver.find_elements(By.CLASS_NAME, '//a[@class="Anchor_anchor__cSc3P RosterRow_playerLink__qw1vG"]').click()

click = driver.find_elements(By.XPATH, '//Select[@name="TEAM_NAME"]').select_by_index(1)
click.select_by_index(0)

select_list = []
for value in click:
    a = value.text
    select_list.append(a)

print(select_list)'''

