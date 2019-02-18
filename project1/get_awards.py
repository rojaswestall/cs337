import gg_api
import award_people
import host
import json
import pymongo
import atexit
from stanfordcorenlp import StanfordCoreNLP
import re
import utils
import pprint

import pandas as pd
import numpy as np
import scipy
import nltk
from nltk.corpus import stopwords
from collections import Counter


# Connect to the Mongo Client
client = pymongo.MongoClient()

# Open the config file and set the correct db and collection
f = open('config.json')
CONFIG = json.load(f)
db = client[CONFIG["dbName"]]
f.close()

# Open the Stanford CoreNLP Pipeline
nlp = StanfordCoreNLP('http://localhost', port=9000)


#def get_awards():
    # identify the key words that will be used to search tweets that contain
    # complete award name
#award_search_keywords = "congratulations congrats cong win receive introduce announce pronounce best award"

#award_tweets = db['gg2013'].find({"$text" : {"$search" : 'best award - "Golden Globes"'}})
award_tweets = db['gg2013'].find({"$text" : {"$search" : 'best award'}}).limit(5000)
tweet_raw_text = [tweet['text'] for tweet in award_tweets]


def clean_tweet(tweet):
    # remove hashtags
    tweet = re.sub(r'#[a-zA-Z]+\b', '', tweet)
    # remove @mentions, urls
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
    # remove 'RT'
    tweet = re.sub(r'\bRT\b', '', tweet)
    return tweet


def normalize_tweet(tweet):
    # clean tweet 
    tweet = clean_tweet(tweet)
    # convert all words to lower case
    tweet_lower = tweet.lower()
    # tokenize all tweet text
    tweet_tokens = nltk.word_tokenize(tweet_lower)

    # default nltk stop words
    stop_words_nltk = stopwords.words('english')
    # need to add some stop words that we dont want
    stop_words_GG = stop_words_nltk + ['golden', 'globes', 'goldenglobes']
    # need to remove some stopwords for the sake of identifying awards
    stopwords_need = ['by', 'an', 'a', 'in', 'or', 'for', 'any']
    stop_words_GG = [stopword for stopword in stop_words_GG if stopword not in stopwords_need]
    # remove stop words previously defined
    tweet_normalized_text = [word for word in tweet_tokens if word not in stop_words_GG]

    return tweet_normalized_text


def chunk_tweet(tweet_tokens):
    # pos tagging tweet tokens
    tweet_pos_tags = nltk.pos_tag(tweet_tokens)
    # chunking part: should be having three different chunkers
    # case 1: type of award named after an individual
        # e.g. firstName middleName lastName award
    chunkGram1 = r"""Chunk: {<NN>{4}}"""  
    # case 2: type of award starts with adjective, followed by multiple nouns, and ends by a noun
    chunkGram2 = r"""Chunk: {<JJS>{1}<JJ>?.*<NN>{2}.*<JJ>?<CC>?<NN>{1}}"""
    # case 3: type of award starts with adjective, 
    chunkGram3 = r"""Chunk: {<JJS>{1}<NN>{1}.*<IN>{1}<DT>{1}.*<NN>{2,}.*<NN>{1}}"""
    
    matches = get_phrases_from_chunks(chunkGram1, tweet_pos_tags) + get_phrases_from_chunks(chunkGram2, tweet_pos_tags) + get_phrases_from_chunks(chunkGram3, tweet_pos_tags)

    if matches == []:
        return None
    return matches

def get_phrases_from_chunks(chunk_gram, tweet_pos):
    chunkParser = nltk.RegexpParser(chunk_gram)
    chunked = chunkParser.parse(tweet_pos)
    matches = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        leaves_words = [ leaf[0] for leaf in subtree.leaves() ]
        phrase = ' '.join(leaves_words)
        matches.append(phrase)

    return matches



# extract all text
tweet_normalized_text = [normalize_tweet(raw_tweet) for raw_tweet in tweet_raw_text]
tweet_chunks = [chunk_tweet(tweet_tokens) for tweet_tokens in tweet_normalized_text if chunk_tweet(tweet_tokens) is not None]
pprint.pprint(utils.flatten(tweet_chunks))

c = Counter(utils.flatten(tweet_chunks))
top20 = c.most_common(20)
print(top20)


awards_short_1819 = [
'cecil b demille award',
'best motion picture - animated', 
'best motion picture - foreign language', 
'best motion picture - drama', 
'best motion picture - musical or comedy',
'best director - motion picture',
'best screenplay - motion picture',
'best original score - motion picture', 
'best original song - motion picture', 
'best television series - drama', 
'best television series - musical or comedy',
'best television limited series or motion picture made for television']

awards_long_1819 = [
'best performance by an actress in a motion picture - drama', 
'best performance by an actor in a motion picture - drama', 
'best performance by an actress in a motion picture - musical or comedy', 
'best performance by an actor in a motion picture - musical or comedy', 
'best performance by an actress in a television series - drama', 
'best performance by an actor in a television series - drama', 
'best performance by an actress in a television series - musical or comedy', 
'best performance by an actor in a television series - musical or comedy', 
'best performance by an actress in a supporting role in any motion picture', 
'best performance by an actor in a supporting role in any motion picture', 
'best performance by an actress in a limited series or a motion picture made for television', 
'best performance by an actor in a limited series or a motion picture made for television', 
'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 
'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 
]

awards_short_1315 = [
'best animated feature film',
'best foreign language film',
'best motion picture - drama',
'best motion picture - comedy or musical',
'best director - motion picture',
'best screenplay - motion picture',
'best original score - motion picture',
'best original song - motion picture',
'best television series - drama',
'best television series - comedy or musical',
'best mini-series or motion picture made for television']

[nltk.pos_tag(normalize_tweet(award)) for award in awards_short_1819]
