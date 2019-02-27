import re
import utils
from utils import safe_run_hosts

import nltk
from nltk.corpus import stopwords
from collections import Counter

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

@safe_run_hosts
def award_names(collection, nlp):
    award_tweets = collection.find({"$text" : {"$search" : 'best'}})
    tweet_raw_text = [tweet['text'] for tweet in award_tweets]

    # extract all text
    tweet_normalized_text = [normalize_tweet(raw_tweet) for raw_tweet in tweet_raw_text]
    tweet_chunks = utils.flatten([chunk_tweet(tweet_tokens) for tweet_tokens in tweet_normalized_text if chunk_tweet(tweet_tokens) is not None])

    c = Counter(tweet_chunks)
    top26 = c.most_common(26)
    top50 = c.most_common(50)
    awards = utils.entities_over_threshold(top50, len(tweet_chunks), 0.05)
    for award in awards: print(award)
    print(top50)

    return awards
