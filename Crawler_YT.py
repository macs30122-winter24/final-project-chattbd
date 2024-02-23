## Web Crawler for YouTube
# Crawling the following:
# Fox News: 
    # https://www.youtube.com/playlist?list=PLlTLHnxSVuIyMU4Q4I8NsLAVK1iNANGW9  
# CNN:
    # https://youtube.com/playlist?list=PL6XRrncXkMaU55GiCvv416NR2qBD_xbmf 
# Al Jazeera: 
    # https://www.youtube.com/playlist?list=PLzGHKb8i9vTzMMCXlnEHxb8QLwE80xorb

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
import regex as re 
import time
from PIL import Image
from io import BytesIO

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless=new')

# Setting up the Chromedriver
service = Service() # A copy of my chromedriver is in the same path as this script
driver = webdriver.Chrome(service = service, options = options)
driver.implicitly_wait(20)

def scroll():
    ''' ADD DOC STRINGS HERE!!!'''
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # Adjust based on loading time
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def gather_links(url):
    ''' ADD DOC STRINGS HERE!!!'''
    driver.get(url)
    scroll()
    return driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    
def gather_all_links(urls_lst, channels_lst):
    ''' ADD DOC STRINGS HERE!!!'''
    links_dict = {}

    for i, e in enumerate(urls_lst):
        comments = gather_links(e)
        links_dict[channels_lst[i]] = comments
    
    for k, v in links_dict.items():
        counter = 0
        lst_urls = []
        for i in v:
            if i.get_attribute("href") == None:
                continue
            url_new = i.get_attribute("href")
            # to get absolute URL w/o reference to playlist:
            url_new = url_new[:url_new.index("&")]
            if url_new[0:4] != "http":
                url_new = "https://www.youtube.com" + url_new
            lst_urls.append(url_new)
            counter +=1
            print('link gathered' + str(counter))
        
        links_dict[k] = lst_urls

    driver.close() # cannot close w/o extracting info; when you try to
        # extract info after, it just gives invalid session id
    driver.quit()
    return links_dict

playlist_urls = [
    ['https://www.youtube.com/playlist?list=PLzGHKb8i9vTzMMCXlnEHxb8QLwE80xorb'],
    'https://youtube.com/playlist?list=PL6XRrncXkMaU55GiCvv416NR2qBD_xbmf',
    'https://www.youtube.com/playlist?list=PLlTLHnxSVuIyMU4Q4I8NsLAVK1iNANGW9' 
    ]

channels_lst = ['Al Jazeera English', 'CNN', 'Fox News']

#links_dict = gather_all_links(playlist_urls, channels_lst)

# Testing CNN only, since it has the smallest number of links