import re
from collections import Counter

import spacy
nlp_spacy = spacy.load('en')


DOCUMENT_SIZE = 10000

def safe_run_hosts(func):

  def func_wrapper(*args, **kwargs):

    try:
      return func(*args, **kwargs)

    except Exception as e:

      print(e)
      return []

  return func_wrapper

def safe_run_process_award(func):
   
  def func_wrapper(*args, **kwargs):

    try:
      return func(*args, **kwargs)

    except Exception as e:

      print(e)
      return '', [], [] # winner, nominees, presenter

  return func_wrapper

# Combine entities of the same type that are right next to each other in text
# This lets us get full names and movies/shows with multiple names
# entities is a list of tuples of (string, type-of-entity)
# entity_type is the type that we are looking to combine
def get_names_and_combine_adjacent_entities(entities, entity_type):
  new_entities = []

  for i, entity in enumerate(entities):
    current_type = entity[1]
    current_name = entity[0]
    if current_type != entity_type:
      continue
    # if the previous entity has the same type
    if len(new_entities) > 0 and entities[i-1][1] == entity_type:
      new_entities[-1] += ' ' + current_name
    else:
      new_entities.append(current_name)

  return new_entities

def combine_adjacent_entities(entities):
  new_entities = []

  for i, entity in enumerate(entities):
    current_type = entity[1]    
    current_name = entity[0]

    # if the previous entity has the same type as the current entity
    if len(new_entities) > 0 and entities[i-1][1] == current_type:
      new_entities[-1] = (new_entities[-1][0] +' ' + current_name, current_type)
    else:
      new_entities.append(entity)

  return new_entities


# Using regular expressions to clean a tweet's text
# Removes hashtags, @mentions, urls, and retweet tag 'RT'
# tweet is the text of a tweet
def clean_tweet(tweet):
  tweet = re.sub(r'#[a-zA-Z]+\b', '', tweet)
  tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
  tweet = re.sub(r'\bRT\b', '', tweet)
  return tweet

# To split a string into multiple strings of 10,000 characters so any one string isn't too large
def split_count(paragraph, x):
  return [paragraph[i: i + x] for i in range(0, len(paragraph), x)]

# Flatten a list of sublists to be just a list
def flatten(lst):
  return [item for sublist in lst for item in sublist]

# return corpus ready for nlp from list of tweets
def corpify_tweets(tweets):
  tweets_text = ' '.join([ tweet['text'] for tweet in tweets ])
  clean_text = clean_tweet(tweets_text)
  corpus = split_count(clean_text, DOCUMENT_SIZE)
  return corpus

# return PERSON entities from corpus
def get_people(corpus, nlp):
  return get_entities(corpus, nlp, people_from_document)

# return entities recognized by entity_recognizer from corpus
def get_entities(corpus, nlp, entity_recognizer):
  pos = [ entity_recognizer(doc, nlp) for doc in corpus ]
  p_nouns = flatten(pos)
  lowered = [ noun.lower() for noun in p_nouns ]
  return lowered

# return PERSON entities from doc
def people_from_document(doc, nlp):
  named_entities = nlp.ner(doc)
  people = get_names_and_combine_adjacent_entities(named_entities, 'PERSON')
  return people

  # return n most common entities
def choose_best_entities(entities, n):
  c = Counter(entities)

  c = boost_full_names(c)

  top_entities = c.most_common(n)
  # top10 = c.most_common(10)
  # a = [ n + ' ' + str(c) for n,c in top10 ]
  # print(' '.join(a))
  # if not is_person:
  #   top_entities = [(name, count) for name, count in top10 if not is_person_entity(name, db_collection, nlp) ]
    
  return [ name for name, _count in top_entities[:n] ] if top_entities else []

def boost_full_names(c):
  name_count_pairs = list(c.items())

  for i, entity in enumerate(name_count_pairs):
    key = entity[0]
    count = entity[1]
    for key2, count2 in name_count_pairs:
      if key == key2:
        continue
      if key2 in key and count > count2:
        c[key] += count2
  return c

THRESHOLD = .1

def choose_entities_over_threshold(entities):
  c = Counter(entities)
  c = boost_full_names(c)

  top10 = c.most_common(10)
  # a = [ n + ' ' + str(c) for n,c in top10 ]
  # print(' '.join(a))
      
  top_entities = entities_over_threshold(top10, len(entities), THRESHOLD)

  return top_entities

def entities_over_threshold(top10, n_entities, threshold):
  top_rate = top10[0][1] / n_entities

  top_entities = [ name for name, count in top10 if top_rate - (count / n_entities) < threshold ]

  return top_entities

def is_person_entity(name, db_collection, nlp):
  tweets = db_collection.find({ '$text': { '$search': name }}).limit(50)
  corpus = corpify_tweets(tweets)
  combed_entities = flatten([ all_entities_from_document(doc, nlp) for doc in corpus])
  labels = [ label for name, label in combed_entities if name.lower() == name ]
  c = Counter(labels)
  classifaction = c.most_common(1)[0]
  return classifaction == 'PERSON'

def all_entities_from_document(doc, nlp):
  named_entities = nlp.ner(doc)
  entities = combine_adjacent_entities(named_entities) 
  return entities

def minus(search_str):
  arr = search_str.split()
  return ' '.join([ '-' + s for s in arr ])
  
#################### legacy code #################

# def tf_idf(entity, db_collection):
#   df = count_query(entity[0], db_collection)
#   idf = math.log10(collection_size / df)
#   return entity[0], entity[1]*idf

def double_quotes(search_str):
  arr = search_str.split()
  return ' '.join([ '"' + s + '"' for s in arr ])

PEOPLE_WORDS = ['actress','actor', 'director', 'producer']
DEAD_WORDS = [ 'performance', 'best', 'role', 'made', 'television']

def is_person_award(award_name):
  return any([ word in award_name for word in PEOPLE_WORDS ])

def award_to_query(award_name):
  document = nlp_spacy(award_name)
  
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct or token.text in DEAD_WORDS) ]
  arr = list(set(arr))
  query = ' '.join([ '"' + s + '"' for s in arr ])
  
  if not is_person_award(award_name):
    query += ' ' + minus(' '.join(PEOPLE_WORDS))
    
  return query

def award_to_soft_query(award_name):
  document = nlp_spacy(award_name)
  
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct or token.text in DEAD_WORDS) ]
  arr = list(set(arr))
  query = ' '.join([ s for s in arr ])

  return query

# import datetime
# Useful functions we use to find when the awards were awarded
# def sortByTime(cursor):
#   time_dict = {}
#   for i, tweet in enumerate(cursor):
#       tm = tweet['timestamp_ms']
#       # Only care about the 100 second period so use -6
#       shortened = str(tm)[:-5]
#       if shortened in time_dict:
#           time_dict[shortened] +=1
#       else:
#           time_dict[shortened] = 1
#   return time_dict

# tweets = db[collection].find({ "$text": { "$search": '"best director - motion picture"'}})
# dic = sortByTime(tweets)
# for key, value in sorted(dic.items()):
#     epoch = datetime.datetime.fromtimestamp(int(key + "00000")/1000.0)
#     readable = epoch.strftime('%I:%M:%S')
#     print(readable, ": ", value)

# Search for tweets in a certain time
# {timestamp_ms: {$gt: 1358090460000, $lt: 1358090700000}}
