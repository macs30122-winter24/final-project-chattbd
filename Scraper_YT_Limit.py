# Importing needed packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options

import requests
import urllib
from numpy.random import default_rng
import random
import time
from PIL import Image
from io import BytesIO
import csv

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless=new')
#options.add_argument('--disable-dev-shm-usage') #  new # Making it slower?
#options.add_argument('--blink-settings=imagesEnabled=false') # new
# also disabled video autoplay

# Setting up the Chromedriver
service = Service() # A copy of my chromedriver is in the same path as this script
driver = webdriver.Chrome(service = service, options = options)
driver.implicitly_wait(20)

# Setting up sleep
rng = default_rng()
time_to_sleep = rng.uniform(1, 3)

# Scrolling
def scroll():
    ''' ADD DOC STRINGS HERE!!!'''
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(5)  # Adjust based on loading time
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def expand_and_check():
    ''' ADD DOCSTRING HERE!!!! '''
    action = ActionChains(driver) 

    # To open description box:
    try:
        e = driver.find_element(By.XPATH, '//*[@id="expand"]')
    except:
        return False, 'No Description box, possibly age registriction'
    action.click(on_element = e) # click the item
    action.perform() # perform the operation 

    date = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text

    month, year = date[:3], date[-4:]
    acceptable_months = ['Oct', 'Nov', 'Dec']
    acceptable_year = '2023'

    if month in acceptable_months and year == acceptable_year:
        return True, 'Moving on'
    else:
        return False, 'Out of range'

def metadata_collect():
    ''' ADD DOCSTRING HERE!!!!'''
    # Title
    title = driver.find_element(By.XPATH, '//*[@id="title"]/h1').text
    # Date
    date = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
    # Channel Name
    channel = driver.find_element(By.XPATH, '//*[@id="text"]/a').text 

    return title, channel, date

def transcript_collect():
    ''' ADD DOCSTRING HERE!!!!!'''
    # To 'Show Transcript':
    action = ActionChains(driver)
    time.sleep(2)

    try:
        e2 = driver.find_element(By.XPATH, \
        '//*[@id="primary-button"]/ytd-button-renderer/yt-button-shape/button')
    except:
        return 'Unable to obtain transcript'

    action.click(on_element = e2)
    action.perform() 

    # Transcript
    try:
        transcript = driver.find_element(By.XPATH,\
             '//*[@id="content"]/ytd-transcript-search-panel-renderer').text
    except: 
        return 'Unable to obtain transcript'
    
    return transcript

def comment_collect():
    ''' ADD DOCSTRING HERE!!!!'''
    comments = driver.find_elements(By.XPATH,
                                     '//*[@id="content-text"]')
    
    comments_lst = []

    for comment in comments:
        comments_lst.append(comment.text)

    return comments_lst

def boss_scraper(links_dict, checked_indexes = [], gathered = 0):
    ''' DO NOT FORGET DOCSTRINGS HERE!!!'''
    global driver

    with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Check if the file is empty (write header if needed)
        if csvfile.tell() == 0:
            csv_writer.writerow(['channel_key', 'channel', 'title', 'date',
                                 'transcript', 'comments'])

        for k, v in links_dict.items():
            counter = 0
            while True:
                s = random.randint(0, len(v)-1)

                if s not in checked_indexes:
                    checked_indexes.append(s)

                    url = v[s] # v is a list of urls
                    driver.get(url)
                    time.sleep(time_to_sleep)

                    WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      'h1.ytd-watch-metadata'))
                    )

                    check, reason = expand_and_check()
                    if not check:
                        if reason == \
                            'No Description box, possibly age registriction':
                            csv_writer.writerow([k, url, 'NA', 'NA', 'NA', 'NA'])
                        continue

                    title, channel, date = metadata_collect()
                    transcript = transcript_collect()
                    scroll()
                    comments = comment_collect()
                    csv_writer.writerow([k, channel, title, date, transcript, 
                                         comments])
                    counter += 1
                    print(counter)
                    print(checked_indexes)

                    if counter >= 255 - gathered:
                        break

                    if counter % 20 == 0: # Every 20 URL visited
                        driver.delete_all_cookies() # clear cookies
                        driver.execute_script("window.localStorage.clear()")
                        driver.close()
                        driver.quit() # close & restart a driver object
                        driver = webdriver.Chrome(service = service, options = options)
                        driver.implicitly_wait(20)

    driver.close()
    driver.quit()


# pd.DataFrame.from_dict(scraped_dict)
# each key is now a column, with its values representing rows

