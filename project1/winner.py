import spacy
import pymongo
# from spacy import displacy
from collections import Counter
import math
import re
import json
import atexit

import logging
from stanfordcorenlp import StanfordCoreNLP
nlp = spacy.load('en')

nlpStan = StanfordCoreNLP('http://localhost', port=9000)

BUCKET_SIZE_SEC = 50 
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

def name(award_name, db_collection, collection_size):
  print(award_name)
  query_str = award_to_query(award_name)
  interval = award_interval(query_str, db_collection)
  if not interval: return ''
  relevant_tweets = db_collection.find({ 'timestamp_ms': { '$gt':interval[0], '$lt':interval[1] }, '$text': { '$search': 'win won congratulations congrats' }} ).limit(1000).sort('timestamp_ms', 1)
  # relevant_tweets = db_collection.find({ 'timestamp_ms': { '$gt':interval[0] }, '$text': { '$search': query_str }} ).limit(200).sort('timestamp_ms', 1)
  # relevant_tweets = db_collection.find({ '$text': { '$search': query_str }} )
  
  
  tweets_text = ' '.join([ tweet['text'] for tweet in relevant_tweets ])
  clean_text = clean_tweet(tweets_text)
  documents = splitCount(clean_text, 10000)
  category = choose_category(award_name)
  top_entity = entities(documents, category, db_collection, collection_size)
  winner = top_entity[0] if top_entity else ''
  print('winner', winner, '\n')
  return winner

def splitCount(s, count):
  return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]


def award_interval(query_str, db_collection):
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

def works_of_art(tweet, entity_type):
  # print('poop', type(tweet))
  entities = nlpStan.ner(tweet)
  # no_os = [ (name.lower(),t) for name, t in entities if t != 'O' ]
  # les_mis = [ (name, t) for name, t in no_os if 'les' in name or 'mis' in name ] 

  # for e in les_mis: print(e)
  named_entities = combine_names(entities, entity_type) # if category == 'PERSON' else non_people(entities)

  return named_entities

def non_people(entities):
  things = [ name for name, ent_type in entities if ent_type != 'PERSON' and ent_type != 'O' ]
  return things

def combine_names(entities, entity_type):
  new_entities = []

  for i, entity in enumerate(entities):
    current_type = entity[1]    
    current_name = entity[0]
    # print(entities)
    if current_type != entity_type:
      continue

    if len(new_entities) > 0 and entities[i-1][1] == entity_type:

      new_entities[-1] += ' ' + current_name

    else:
      new_entities.append(current_name)

  return new_entities

def choose_category(award_name):
  people_words = ['actress','actor', 'director']
  if any([ word in award_name for word in people_words ]):
    return 'PERSON'
  else:
    return 'ORGANIZATION'

def entities(documents, category, db_collection, collection_size):
  arts = [ works_of_art(tweets_text, category) for tweets_text in documents ]
  flat_arts = flatten(arts)
  c = Counter(flat_arts)

  # if category == 'WORK_OF_ART':
  #   top_entities = c.most_common(10)
  #   print(top_entities)
  #   idf_entities = [ tf_idf(entity, db_collection, collection_size) for entity in top_entities ]
  #   return max(idf_entities, key=lambda x: x[1]) if idf_entities else None
  
  # else:
  top_entities = c.most_common(1)
  print(c.most_common(5))
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


# Connect to the Mongo Client
client = pymongo.MongoClient()

# Open the config file and set the correct db and collection

f = open('config.json')
data = json.load(f)
collection = data["dbCollection"]
db = client[data["dbName"]]
f.close()

COLLECTION_SIZE = db[collection].count_documents({})

# print(award_to_query('best performance by an actress in a television series - comedy or musical'))
b = [
# 'cecil b. demille award',
#  'best motion picture - drama',
 'best performance by an actress in a motion picture - drama',
#  'best performance by an actor in a motion picture - drama',
 'best motion picture - comedy or musical',
#  'best performance by an actress in a motion picture - comedy or musical',
#  'best performance by an actor in a motion picture - comedy or musical',
#  'best animated feature film',
#  'best foreign language film',
#  'best performance by an actress in a supporting role in a motion picture',
#  'best performance by an actor in a supporting role in a motion picture',
#  'best director - motion picture',
#  'best screenplay - motion picture',
#  'best original score - motion picture',
#  'best original song - motion picture',
#  'best television series - drama',
#  'best performance by an actress in a television series - drama',
#  'best performance by an actor in a television series - drama',
#  'best television series - comedy or musical',
#  'best performance by an actress in a television series - comedy or musical',
#  'best performance by an actor in a television series - comedy or musical',
#  'best mini-series or motion picture made for television',
#  'best performance by an actress in a mini-series or motion picture made for television',
#  'best performance by an actor in a mini-series or motion picture made for television',
#  'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
#  'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television',
 ]

def exit_handler():
  nlpStan.close()

atexit.register(exit_handler)
# asd = clean_tweet('RT @RobstenLovex: RT @ROBsessedBlog: Awwwww RT @RPattzgirl: Awwww  RT @epnebelle: And a real smile on Rob #GoldenGlobes http://t.co/JXatOwdJ')
# print(asd)
# for award in b:
#   name(award, db[collection], COLLECTION_SIZE)
# a = [ award_to_query(award) for award in b]
# for c in a: print(c)
# d = nlpStan.ner("#GoldenGlobes for best picture to Argo over Lincoln! C'mon Argo is a good movie but Lincoln is awesome!! #ripoff #Argo")
# print(d)



