import spacy
import pymongo
from spacy import displacy
from collections import Counter
import math
import re
nlp = spacy.load('en')

BUCKET_SIZE_SEC = 50 
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

def name(award_name, db_collection, collection_size):
  print(award_name)
  query_str = award_to_query(award_name)
  interval = foo(query_str, db_collection)
  if not interval: return ''
  tweets = db_collection.find({ 'timestamp_ms': { '$gt':interval[0], '$lt':interval[1] }, '$text': { '$search': 'win won congrat' }} ).limit(100).sort('timestamp_ms', 1)

  tweet_text = [ clean_tweet(tweet['text']) for tweet in tweets ]

  category = choose_category(award_name)
  top_entities = entities(tweet_text, 1, category)
  winner = top_entities[0][0] if top_entities else ''
  print('winner', winner, '\n')
  return winner

def foo(query_str, db_collection):
  tweets = db_collection.find({ "$text": { "$search": query_str } })
  buckets = [ tweet['timestamp_ms'] // BUCKET_SIZE_MS for tweet in tweets ]
  if not buckets: return None
  c = Counter(buckets)
  peak = c.most_common(1)
  peak = peak[0][0] * BUCKET_SIZE_MS
  interval = [peak, peak+(BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS) ]
  return interval

def getBestFromList(lst):
    return list(reversed(sorted(lst, key=lambda x: x[1])))

def query(search_str, db_collection):
    return db_collection.find({ "$text": { "$search": search_str }})

def double_quotes(search_str):
  arr = search_str.split()
  return ' '.join([ '"' + s + '"' for s in arr ])

def count_query(search_str, db_collection):
    return db_collection.count_documents({ "$text": { "$search": search_str }})

def tf_idf(entity, db_collection, collection_size):
    df = count_query(entity[0], db_collection)
    idf = math.log10(collection_size / df)
    return entity[0], entity[1]*idf

def works_of_art(tweet, category):
  document = nlp(tweet)

  # works = filter(lambda x: x.label_ == 'WORK_OF_ART', document.ents)
  works = [ x.text for x in document.ents if x.label_ == category ]
  # items = [ x.text for x in works ]
  return works

def choose_category(award_name):
  people_words = ['actress','actor', 'director']
  if any([ word in award_name for word in people_words ]):
    return 'PERSON'
  else:
    return 'WORK_OF_ART'

def entities(tweets, n, category):
  arts = flatten([ works_of_art(tweet, category) for tweet in tweets ])
  c = Counter(arts)
  top_entities = c.most_common(n)
  return top_entities

def flatten(lst):
  return [item for sublist in lst for item in sublist] 

def award_to_query(award_name):
  document = nlp(award_name)
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct) ]
  query = ' '.join([ '"' + s + '"' for s in arr ])
  return query

def clean_tweet(tweet):
  tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
  tweet = re.sub(r'\bRT\b', '', tweet)
  return tweet

# print(award_to_query('best performance by an actress in a television series - comedy or musical'))
