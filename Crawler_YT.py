## Web Crawler for YouTube
''' 
This code takes in a list of channel names and a list of playlist URLS, and
then gathers all links in each playlist. It then returns a dictionary, which we
can save as CSV for use later with our scraper without having to rerun the 
crawler every time.
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options

import time
import csv

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless=new')

# Setting up the Chromedriver
service = Service() # A copy of chromedriver is in the same path as this script
driver = webdriver.Chrome(service = service, options = options)
driver.implicitly_wait(20)

def scroll():
    '''
    This function scrolls all the way to the end of the playlist. 

    Input: None
    Returns: None
    '''
    last_height = driver.execute_script\
        ("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script\
            ("window.scrollTo(0, document.documentElement.scrollHeight);")
        # Adjust based on loading time, otherwise not all video links 
        # will be grabbed: 
        time.sleep(5)
        new_height = driver.execute_script\
            ("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def gather_links(url):
    '''
    This function gathers all elements by XPATH that will hold links for videos.

    Input: None
    Returns: a list of driver objects/elements.
    '''
    driver = webdriver.Chrome(service = service, options = options)
    driver.implicitly_wait(20)
    driver.get(url)
    scroll()
    return driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    
def gather_all_links(urls_lst, channels_lst):
    ''' 
    The function that brings everything together to crawl all playlists of 
    interest.

    Inputs:
        urls_lst (list): a list of playlist links
        channels_lst (list): a playlist of channel names, ordered in the same
            way as the urls_lst
    
    Returns:
        links_dict (dictionary): a dictionary, where the keys are the channels'
            names and the values are lists of video links.
    '''
    links_dict = {}

    for i, e in enumerate(urls_lst):
        lst_urls = []
        playlist_links = gather_links(e)
    
        for link in playlist_links:
            if link.get_attribute("href") == None:
                continue

            url_new = link.get_attribute("href")

            # to get absolute URL w/o reference to playlist:
            url_new = url_new[:url_new.index("&")]

            if url_new[0:4] != "http":
                url_new = "https://www.youtube.com" + url_new

            lst_urls.append(url_new)

        links_dict[channels_lst[i]] =  lst_urls
    
    driver.quit()
    return links_dict

###############################################################################

channels_lst = ['Al Jazeera English', 'CNN', 'Fox News']
playlist_urls = [
    'https://www.youtube.com/playlist?list=PLzGHKb8i9vTzMMCXlnEHxb8QLwE80xorb',
    'https://youtube.com/playlist?list=PL6XRrncXkMaU55GiCvv416NR2qBD_xbmf',
    'https://www.youtube.com/playlist?list=PLlTLHnxSVuIyMU4Q4I8NsLAVK1iNANGW9' 
    ]

links_dict = gather_all_links(playlist_urls, channels_lst)

# To save as a CSV file:

with open('links_to_scrape.csv', 'w') as f1:
    w = csv.writer(f1)
    for k, v in links_dict.items():
        w.writerow([k,v])

# Manually separated the CSV files into 3 separate files as to facilitate
# dealing w/ the Scraper, but everything is built to be handled automatically
# if needed/possible. I did this mainly to facilitate the scraper due to its
# computationally and time intensive processes. 

## Resources:
# Lecture notebook on dynamic webscraping 
# https://pythonspot.com/save-a-dictionary-to-a-file/ 
# https://formulae.brew.sh/cask/chromedriver
# https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location/ 
# https://stackoverflow.com/questions/68408692/why-window-scrollto-doesnt-work-with-pages-like-youtube