def get_tables(year, url):
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import pandas as pd 
    import time

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(PATH, options=options)
    website = '{}{}'.format(url, year)
    driver.get(website)


    matches = driver.find_elements(By.XPATH, "//tr[@class='Crom_headers__mzI_m']/th")
    headers = [match.text for match in matches]

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
    driver.close()
    return df
