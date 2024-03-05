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

from numpy.random import default_rng
import random
import time
import csv
import pandas as pd

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless=new')

# Setting up the Chromedriver
service = Service() # A copy of chromedriver is in the same path as this script
driver = webdriver.Chrome(service = service, options = options)
driver.implicitly_wait(20)

# Setting up sleep
rng = default_rng()
time_to_sleep = rng.uniform(1, 3)

# Scrolling
def scroll():
    '''
    This function scrolls all the way to the end of the video page.

    Input: None
    Returns: None
    '''
    last_height = driver.execute_script\
        ("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script\
            ("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(5)  # Adjust based on loading time
        new_height = driver.execute_script\
            ("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def expand_and_check():
    '''
    This function expands the description box on the YouTube video and checks
    the date to make sure it is within timeframe. Given that our time frame is
    between Oct - Dec 2023. 

    Inputs: None
    Returns:
        check (boolean): True if the video falls within our time frame, 
            false if it does not.
        Reason (string): gives us the reason of not moving on with the video
            is it a time constraint or is there no description box due to
            age restrictions imposed by YouTube that would force us to sign in
            to overcome them. 
    '''
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
    ''' 
    This functions collects the metadata we are interested in, such as 
    title, date, and channel.

    Input: None
    Returns:
        title, channel, date (tuple of strings): metadata we are interested in.
    '''
    # Title
    title = driver.find_element(By.XPATH, '//*[@id="title"]/h1').text
    # Date
    date = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
    # Channel Name
    channel = driver.find_element(By.XPATH, '//*[@id="text"]/a').text 

    return title, channel, date

def transcript_collect():
    '''
    This function clicks on "Show transcript" button if it is available, and 
    collects all of the transcript script.

    Input: None
    Returns:
        transcript (string): if available, returns script. If not, it returns
        "Unable to obtain transcript"
    '''
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
    transcript = driver.find_element(By.XPATH,\
             '//*[@id="content"]/ytd-transcript-search-panel-renderer').text
    
    return transcript

def comment_collect():
    '''
    This function collects all elements/objects related to comments, then turns 
    each one to text and saves them in a list.
    
    Input: None
    
    Returns: 
        comments_lst (list of strings): the obtained comments, returns empty
            list if there are no comments gathered/no comments available.
    '''
    comments = driver.find_elements(By.CSS_SELECTOR,
                                     ".style-scope ytd-comment-renderer")

    comments_lst = []

    for comment in comments:
        comments_lst.append(comment.text)

    return comments_lst

def boss_scraper(links_dict, output_file_name):
    '''
    The function that brings everything together and scrapes each video link,
    gathers needed information and writes them to a CSV file as it goes on.
    
    Input:
        links_dict (dictionary): a dictionary of channel and crawled playlist
            URLS.
        
        output_file_name (string): the name of the output file with .csv
            extension.
    
    Returns: None, automatically creates & writes to CSV file.
    '''
    global driver
    with open(output_file_name, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Check if the file is empty (write header if needed)
        if csvfile.tell() == 0:
            csv_writer.writerow(['channel_key', 'channel', 'title', 'date',
                                 'transcript', 'comments'])

        for k, v in links_dict.items():
            counter = 0
            for url in v:
                driver.get(url)
                time.sleep(time_to_sleep)

                WebDriverWait(driver, 15).until(
                 EC.visibility_of_element_located((By.CSS_SELECTOR, \
                                                   'h1.ytd-watch-metadata')))

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
                #print(counter) # was here to facilitate monitoring of scraping

                if counter % 20 == 0: # Every 20 URL scraped, 
                    driver.delete_all_cookies() #clear cookies
                    driver.execute_script("window.localStorage.clear()")
                    driver.close()
                    driver.quit() # restart a driver object:
                    driver = webdriver.Chrome(service = service, 
                                              options = options)
                    driver.implicitly_wait(20) 

    driver.close()
    driver.quit()


def boss_scraper_limit(links_dict, output_file_name, checked_indexes = [], \
                       gathered = 0):

    '''
    The limited version of the function that brings everything together and 
    scrapes each video link, gathers needed information and writes them to a 
    CSV file as it goes on.
    
    Input:
        links_dict (dictionary): a dictionary of channel and crawled playlist
            URLS.
        
        output_file_name (string): the name of the output file with .csv
            extension.
        
        checked_indexes (list): defaults to an empty list if not provided. 
            In case of driver crash, this would facilitate the restarting of
            the scraping w/o falling in the risk of scraping videos I have
            already scraped before. 
                Worth noting that, once I implemented the restarting of driver
                every 20 URLS visited, it was no longer crashing. However, 
                this functionality is still useful.
        
        gathered (integer): default to 0 if not provided. 
            Similar to the above, if driver crashes or internet loses strength.
            This can help us resume without exceeding the limit we have 
            determined.
    
    Returns: None, automatically creates & writes to CSV file.
    '''
    global driver

    with open(output_file_name, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Check if the file is empty (write header if needed)
        if csvfile.tell() == 0:
            csv_writer.writerow(['channel_key', 'channel', 'title', 'date',
                                 'transcript', 'comments'])

        for k, v in links_dict.items():
            counter = 0
            
            # The following is the part that allows us to randomly select
            # 255 videos of those available in the playlist:

            while True:
                s = random.randint(0, len(v)-1)

                if s not in checked_indexes:
                    checked_indexes.append(s)

                    url = v[s] # v is a list of urls

                    # The rest of the function is mostly the same logic as the 
                    # original function:

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
                    # print(counter) # these were here to facilitate monitoring 
                    # print(checked_indexes) # of scraping progress

                    # This is also different than the original version of
                    # function:
                    if counter >= 255 - gathered:
                        break

                    if counter % 20 == 0: # Every 20 URL scraped,
                        driver.delete_all_cookies() # clear cookies
                        driver.execute_script("window.localStorage.clear()")
                        driver.close()
                        driver.quit() # close & restart a driver object
                        driver = webdriver.Chrome(service = service,
                                                  options = options)
                        driver.implicitly_wait(20)

    driver.close()
    driver.quit()

def df_dict(csv_file):
    ''' 
    This functions turns a csv file into a dataframe, then turns the dataframe
    into a dictionary in the same format needed to run the scraper above.
    
    Input: 
        csv_file (string): name of input file with .csv extension.
    
    Returns:
        dict_new (dictionary): a dictionary with name of channel as key, 
            and value is a list of links to scrape.
    '''

    df = pd.read_csv("csv_file")
    dict_new= {}

    for row in df.itertuples():
        dict_new[row._1] = row._2
    
    return dict_new

###############################################################################
# IMPORTANT Note: we only use the original function for the CNN playlist URLS
# b/c we limit the rest to 255 videos within time frame for computational 
# resources and time constraints as the 255 videos take 8-10 hours. 

cnn_to_scrape_dict = df_dict('links_to_scrape_cnn.csv')
FN_to_scrape_dict = df_dict('links_to_scrape_FN.csv')
AlJazeera_to_scrape_dict = df_dict('links_to_scrape_AlJazeera.csv')

boss_scraper(cnn_to_scrape_dict, "output_cnn.csv")

boss_scraper_limit(FN_to_scrape_dict, "output_AlJazeera.csv")

boss_scraper_limit(AlJazeera_to_scrape_dict, "output_FoxNews.csv")

# Resources:
# https://www.geeksforgeeks.org/selenium-python-tutorial/
# https://www.geeksforgeeks.org/click-method-action-chains-in-selenium-python/
# https://medium.com/analytics-vidhya/scraping-youtube-data-using-python-and-selenium-to-classify-videos-89afde8381c4 
# https://brightdata.com/blog/how-tos/how-to-scrape-youtube-in-python 


