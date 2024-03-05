# Difference in bias between News Media Outlets and Social Media in the Israel - Palestine conflict

## The project
This project delves into the dynamics of media bias in the context of the Israel-Palestine conflict, an issue that has long polarized public opinion and influenced foreign policy and humanitarian aid perspectives. Recognizing the profound impact of media portrayal on societal perceptions, this research aims to enhance media literacy by scrutinizing the emotional language and thematic content across traditional news outlets and social media platforms. The core objective is to uncover the nuances of bias, facilitating a more informed public discourse. Particularly, we were interested in identifying differences in bias between social media and news evidence as evidenced by the language used when discussing topics relating to the conflict at hand. 
To this end, we compiled an extensive dataset comprising 134,204 posts from the r/israelpalestine subreddit, comments and transcripts from 805 YouTube videos across Al Jazeera, CNN, and Fox News, and 1,986 articles from Fox News and CNN. We then used Word2Vec, a word embedding algorithm, to create two semantic models to map the emotional and topical landscape of the discourse surrounding this geopolitical issue.
We then projected a predefined set of emotionally charged and topic-specific words onto an Israel-Palestine dimension, which resulted in a Israel-Palestine score for each word. With this score representing the semantic distance of each word to both sides of the conflict, we conducted a set of t-tests to determine the significance of difference in the means of these scores among the corpora. 
The findings reveal a nuanced landscape of media bias. Emotional bias, characterized by a slant towards Palestine in both corpora, was significantly more pronounced in traditional news media compared to social media. Conversely, topical bias presented a more complex picture; social media maintained a neutral stance overall (an Israel-Palestine core mean close to 0), whereas news media exhibited a distinct Palestine slant. These results underscore significant disparities between the two media types, affirming the presence of distinct emotional and topical biases.
With these results we were able to illustrate that there are indeed substantial differences in media representation of the Israel-Palestine conflict, with traditional news media and social media platforms diverging both in the magnitude and directionality of bias. The alignment of emotional bias towards Palestine across both media types contrasts with the variance observed in topical bias, highlighting a critical area for further investigation.
Looking ahead, the study proposes several avenues for future research. Incorporating a temporal analysis could offer insights into the evolution of media bias over time, particularly in relation to different phases of the conflict. Additionally, a comparative study of media portrayal during various escalations of the conflict could shed light on the consistency of bias across different temporal contexts. Furthermore, exploring syntactic bias, such as the use of active versus passive voice, could deepen the understanding of subtler dimensions of media slant.
In essence, this research contributes to a more nuanced understanding of media bias in the context of the Israel-Palestine conflict. By leveraging advanced semantic modeling techniques, it provides a foundational framework for dissecting media content, paving the way for enhanced media literacy and a more discerning public discourse.
 
## Code in this repo
The code used to scrape, clean and analyze the the data is inside the "code" file inside of this repository. It contains the following files:
### Text_analyzer.ipynb 
Jupyter notebook used to create the lists of words (emotional, topical, israel, palestine), create the israel-palestine dimension, project the words into the dimension and run statistical tests with the results. Visualizations for the embedding space and dimension are also included in this notebook.

### Libraries used in this project
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
- selenium 4.17.2
- csv
- random
- time
- ast

## Data
Some of the data for the project is contained in the "data" folder of this repository. It contains:
- NRC-Emotion-Lexicon-Wordlevel-v0.92.txt: a dictionary of emotional words in english. Used in Text_analyzer.ipynb
- news_word2vec.model: a Word2Vec model of the semantic space in the news corpus
- sm_word2vec.model: a Word2Vec model of the semantic space in the social media corpus
Additionally, data files too large to be stored on github are found in the following links:
- [full data set](https://uchicago.box.com/s/7m1l1qdyuycqhe0qfxobls8f1zi556xp)
- [all news](https://uchicago.box.com/s/c7r3jt7jnz610l98gkt60i2de0yr1gfp)
- [all social media](https://uchicago.box.com/s/pv9jehfqrn32of06w7bauwrp9sgg8t3f)

## Responsabilities in the project

- Alejandro Sarria: Data analysis, data visualization, presentation slides
- Nour Abdelbaki: Youtube scrapping, presentation slides
- Ethan Kozlowski: Reddit scrapping; data processing, analysis, and visualization; presentation slides
- Nalin Bhatt: News websites scrapping

## Slides
The slides for our project are available [here](https://docs.google.com/presentation/d/1EXfl5mTUGFtI3p69C_kS19-dEpcnX3zp/edit?usp=sharing&ouid=100471119288052324164&rtpof=true&sd=true).

## Video
The video presentation for our project is available [here](ADD LINK).
