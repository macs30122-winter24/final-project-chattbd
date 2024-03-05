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
- selenium 4.17.2
- csv
- random
- time
- ast
## Data
The data sources for the project are contained in the "folder" of this repository. It contains:
- NRC-Emotion-Lexicon-Wordlevel-v0.92.txt: a dictionary of emotional words in english. Used in Text_analyzer.ipynb
- news_word2vec.model: a Word2Vec model of the semantic space in the news corpus
- sm_word2vec.model: a Word2Vec model of the semantic space in the social media corpus
- ADD BOX LINKS TO TEXT DATA

## Responsabilities in the project

- Alejandro Sarria: Data analysis, data visualization, presentation slides
- Nour Abdelbaki: Youtube scrapping, presentation slides
- Ethan Kozlowski: Reddit scrapping, data cleaning, data wrangling, data analysis, visualization, presentation slides
- Nalin Bhatt: News websites scrapping

## Slides

## Video
  
