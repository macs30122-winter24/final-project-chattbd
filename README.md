# Difference in bias between News Media Outlets and Social Media in the Israel - Palestine conflict

## The project
- RQS:
- Short summary:
- Main findings: 
## Code in this repo
The code used to scrape, clean and analyze the the data is inside the "code" file inside of this repository. It contains the following files:
### Text analyzer 
Jupyter notebook used to create the lists of words (emotional, topical, israel, palestine), create the israel-palestine dimension, project the words into the dimension and run statistical tests with the results. Visualizations for the embedding space and dimension are also included in this notebook.
The libraries used in this notebook are:
- Gensim 4.3.0
- Numpy 1.24.3
- sklearn 1.3.0
- pandas 2.0.3

### Data_cleaning_processing_etc
Jupyter notebook used to clean up, process, and prepare all data for future analyses. Notebook also used for creating some of the exploratory data analysis visuals. 
The libraries used in this notebook are:
- pandas 2.2.0
- numpy 1.25.2
- beautifulsoup4 4.12.2
- reqyests 2.31.0
- tqdm 4.65.0
- spacy 3.7.2
- gensim 4.3.0
- nltk 3.8.1
- wordlcoud 1.9.3
- seaborn 0.12.2
- sklearn 0.0.post11

### Data gathering
We gathered our data from 4 main sources, Youtube, Reddit, cnn, and foxnews. We implemented dynamic scrappers using selenium to gather the data from Youtube and the news websites. We were able to gather the Reddit data using normal scraping off of the old.Reddit.com website. 
... [ADD MORE]

### Preprocessing
All data came in the form of text. Though we gathered data for time, due to a lack of time, we did incorporate a temporal component to this project. The data processing largely occured in 4 majors steps. The first step was going through all the individual Youtube (Fox, CNN, and Al Jazeera), Reddit posts, and the articles from the news sites. We removed hyperlinks, closed captioning speaker attributions (when necessary for Youtube). We also generally removed any character that did not match this regular expression: r"""[^a-zA-Z\d\s\[\]\-\#\.\?\,\&\<\>\!\@\$\%\^\*\+\=\:\;\\/\%\'\"]""". 

### Analysis
## Data 

## libraries and versions

## Tasks
- Alejandro Sarria: Data analysis and data visualization
- Nour Abdelbaki: Scraping Youtube, 
- Ethan Kozlowski: scraping Reddit, data cleaning, wrangling, analysis, visualization
- Nalin Bhatt: Scraping News websites (CNN, Fox),

## Slides (link)

## Video
  
