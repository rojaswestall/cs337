import spacy
import pymongo
from collections import Counter
import math
import re
import json
import atexit

from stanfordcorenlp import StanfordCoreNLP
nlp = spacy.load('en')

nlpStan = StanfordCoreNLP('http://localhost', port=9000)

BUCKET_SIZE_SEC = 50 
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

def name(award_name, db_collection):
  print(award_name)
  query_str = award_to_query(award_name)
  interval = award_interval(query_str, db_collection)
  print('interval', interval)
  if not interval: return ''
  relevant_tweets = db_collection.find({ 'timestamp_ms': { '$gt': interval[0], '$lt':interval[1] }, '$text': { '$search': 'win won congratulations congrats' }} ).limit(1000).sort('timestamp_ms', 1)
  
  # relevant_tweets = db_collection.find({ 'timestamp_ms': { '$gt':interval[0] }, '$text': { '$search': query_str }} ).limit(200).sort('timestamp_ms', 1)
  # relevant_tweets = db_collection.find({ '$text': { '$search': query_str }} )
  
  
  tweets_text = ' '.join([ tweet['text'] for tweet in relevant_tweets ])
  clean_text = clean_tweet(tweets_text)
  documents = splitCount(clean_text, 10000)
  is_person = is_person_award(award_name)
  top_entity = entities(documents, is_person)

  winner = top_entity[0] if top_entity else ''

  print('winner', winner, '\n')
  return winner

def splitCount(paragraph, x):
  return [paragraph[i: i + x] for i in range(0, len(paragraph), x)]

def award_interval(query_str, db_collection):
  tweets = db_collection.find({ "$text": { "$search": query_str } })
  buckets = [ int(tweet['timestamp_ms']) // BUCKET_SIZE_MS for tweet in tweets ]
  if not buckets: return None
  c = Counter(buckets)
  peak = c.most_common(1) 
  peak = peak[0][0] * BUCKET_SIZE_MS
  interval = [peak, peak+(BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS) ]
  return interval

def query(search_str, db_collection):
    return db_collection.find({ "$text": { "$search": search_str }})

def double_quotes(search_str):
  arr = search_str.split()
  return ' '.join([ '"' + s + '"' for s in arr ])

def count_query(search_str, db_collection):
    return db_collection.count_documents({ "$text": { "$search": search_str }})

# def tf_idf(entity, db_collection):
#     df = count_query(entity[0], db_collection)
#     idf = math.log10(collection_size / df)
#     return entity[0], entity[1]*idf

def works_of_art(tweet, is_person):
  if not is_person:
    return spacify(tweet)

  entities = nlpStan.ner(tweet)
  named_entities = combine_names(entities, 'PERSON') 

  return named_entities

def spacify(tweet):
  poss = nlpStan.pos_tag(tweet)
  return combine_names(poss, 'NNP')

def combine_names(entities, entity_type):

  new_entities = []

  for i, entity in enumerate(entities):
    current_type = entity[1]    
    current_name = entity[0]
    if current_type != entity_type:
      continue

    if len(new_entities) > 0 and entities[i-1][1] == entity_type:

      new_entities[-1] += ' ' + current_name

    else:
      new_entities.append(current_name)

  return new_entities

def is_person_award(award_name):
  people_words = ['actress','actor', 'director']
  return any([ word in award_name for word in people_words ])

def entities(documents, is_person):
  arts = [ works_of_art(tweets_text, is_person) for tweets_text in documents ]
  flat_arts = flatten(arts)
  lowered = [ entity.lower() for entity in flat_arts ] 
  c = Counter(lowered)

  top_entities = c.most_common(1)
  print(c.most_common(10))
  return top_entities[0] if top_entities else None   

def flatten(lst):
  return [item for sublist in lst for item in sublist] 

DEAD_WORDS = [ 'performance', 'best', 'role', 'made', 'television']
def award_to_query(award_name):
  document = nlp(award_name)
  
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct or token.text in DEAD_WORDS) ]
  arr = list(set(arr))
  query = ' '.join([ '"' + s + '"' for s in arr ])

  return query

def clean_tweet(tweet):
  tweet = re.sub(r'#[a-zA-Z]+\b', '', tweet)
  tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
  tweet = re.sub(r'\bRT\b', '', tweet)
  return tweet

def exit_handler():
  nlpStan.close()

atexit.register(exit_handler)
