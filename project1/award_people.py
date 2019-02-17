import spacy
import pymongo
from collections import Counter
import math
import re

nlp_spacy = spacy.load('en')

BUCKET_SIZE_SEC = 50 
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

RELEVANT_TWEETS_LIMIT = 1000

DOCUMENT_SIZE = 10000

def process_award(award_name, db_collection, nlp):
  peak_timestamp = find_peak_activity(award_name, db_collection)
  if not peak_timestamp: return '' , '', ''

  winner = find_winner(award_name, peak_timestamp, db_collection, nlp)
  nominees = find_nominees(peak_timestamp, db_collection, nlp)
  presenters = find_presenters(peak_timestamp, db_collection, nlp)
  print('winner:', winner, 'nominees:', nominees, 'presenters:', presenters, '\n')
  return winner, nominees, presenters

def find_peak_activity(award_name, db_collection):
  query_str = award_to_query(award_name)
  tweets = db_collection.find({ "$text": { "$search": query_str } })
  buckets = [ int(tweet['timestamp_ms']) // BUCKET_SIZE_MS for tweet in tweets ]
  if not buckets: return None

  c = Counter(buckets)
  peak = c.most_common(1) 
  peak_timestamp = peak[0][0] * BUCKET_SIZE_MS
  return peak_timestamp

def find_winner(award_name, peak_timestamp, db_collection, nlp):
  interval = get_relevant_interval(peak_timestamp, 0, 1)
  tweets = relevant_tweets(interval, 'win won congratulations congrats' , db_collection)
  corpus = corpify_tweets(tweets)

  entities = get_people(corpus, nlp) if is_person_award(award_name) else get_proper_nouns(corpus, nlp)
  winner = choose_best_entities(entities, 1)[0]
  return winner

def find_nominees(peak, db_collection, nlp):
  return []
  pass

def find_presenters(peak, db_collection, nlp):
  return []
  pass

def get_relevant_interval(peak, negative_width, positive_width):
  interval = [ 
    peak+(negative_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS),
    peak+(positive_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS), 
    ]
  return interval

def relevant_tweets(interval, query_str, db_collection):
  return db_collection.find(
    { 'timestamp_ms': { 
      '$gt': interval[0], 
      '$lt': interval[1] }, 
      '$text': { '$search': query_str }} 
  ).limit(RELEVANT_TWEETS_LIMIT).sort('timestamp_ms', pymongo.ASCENDING)

def corpify_tweets(tweets):
  tweets_text = ' '.join([ tweet['text'] for tweet in tweets ])
  clean_text = clean_tweet(tweets_text)
  corpus = splitCount(clean_text, DOCUMENT_SIZE)
  return corpus
  
def get_proper_nouns(corpus, nlp):
  return get_entities(corpus, nlp, proper_nouns_from_document)

def get_people(corpus, nlp):
  return get_entities(corpus, nlp, people_from_document)

def get_entities(corpus, nlp, entity_recognizer):
  pos = [ entity_recognizer(doc, nlp) for doc in corpus ]
  p_nouns = flatten(pos)
  return p_nouns

def people_from_document(doc, nlp):
  named_entities = nlp.ner(doc)
  people = combine_names(named_entities, 'PERSON') 
  return people

def proper_nouns_from_document(doc, nlp):
  pos = nlp.pos_tag(doc)
  proper_nouns = combine_names(pos, 'NNP')
  return proper_nouns

def choose_best_entities(entities, n):
  lowered = [ entity.lower() for entity in entities ] 
  c = Counter(lowered)
  name_count_pairs = list(c.items())

  for i, entity in enumerate(name_count_pairs):
    key = entity[0]
    count = entity[1]
    for key2, count2 in name_count_pairs[i+1:]:
      if key2 in key and count > count2:
        c[key] += count2

  top10 = c.most_common(10)
  a = [ n + ' ' + str(c) for n,c in top10 ]
  print(' '.join(a))
  
  top_entities = c.most_common(n)
  
  return [ name for name, _count in top_entities[:n] ] if top_entities else []

def splitCount(paragraph, x):
  return [paragraph[i: i + x] for i in range(0, len(paragraph), x)]

def double_quotes(search_str):
  arr = search_str.split()
  return ' '.join([ '"' + s + '"' for s in arr ])

# def tf_idf(entity, db_collection):
#     df = count_query(entity[0], db_collection)
#     idf = math.log10(collection_size / df)
#     return entity[0], entity[1]*idf

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

def flatten(lst):
  return [item for sublist in lst for item in sublist] 

DEAD_WORDS = [ 'performance', 'best', 'role', 'made', 'television']
def award_to_query(award_name):
  document = nlp_spacy(award_name)
  
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct or token.text in DEAD_WORDS) ]
  arr = list(set(arr))
  query = ' '.join([ '"' + s + '"' for s in arr ])

  return query

def clean_tweet(tweet):
  tweet = re.sub(r'#[a-zA-Z]+\b', '', tweet)
  tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
  tweet = re.sub(r'\bRT\b', '', tweet)
  return tweet
