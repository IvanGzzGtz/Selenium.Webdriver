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


def get_teams():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver1 = webdriver.Chrome(PATH, options=options)
    website = 'https://www.nba.com/players'   
    driver1.get(website)
    x = driver1.find_elements(By.XPATH, '//Select[@name="TEAM_NAME"]/option')
    team_names = []
    for team in x:
        team = team.text
        team_names.append(team)
    
    driver1.close()
    return team_names[1:]
