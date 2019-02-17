import spacy
import pymongo
from collections import Counter
import utils

nlp_spacy = spacy.load('en')

BUCKET_SIZE_SEC = 50 
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

RELEVANT_TWEETS_LIMIT = 800

def process_award(award_name, db_collection, nlp):
  print(award_name)
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
  corpus = utils.corpify_tweets(tweets)

  entities = utils.get_people(corpus, nlp) if is_person_award(award_name) else get_proper_nouns(corpus, nlp)
  winner = utils.choose_best_entities(entities, 1)[0]
  return winner

def find_nominees(peak, db_collection, nlp):
  return []
  pass

def find_presenters(peak, db_collection, nlp):
  interval = get_relevant_interval(peak, 2, 0)
  tweets = relevant_tweets(interval, 'presents presenters introduces intros introducing announce announcing announcers ' , db_collection)
  corpus = utils.corpify_tweets(tweets)
  entities = utils.get_people(corpus, nlp)
  winner = utils.choose_best_entities(entities, 1)[0]
  return winner

def get_relevant_interval(peak, negative_width, positive_width):
  interval = [ 
    peak-(negative_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS),
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

def get_proper_nouns(corpus, nlp):
  return utils.get_entities(corpus, nlp, proper_nouns_from_document)

def proper_nouns_from_document(doc, nlp):
  pos = nlp.pos_tag(doc)
  proper_nouns = utils.get_names_and_combine_adjacent_entities(pos, 'NNP')
  return proper_nouns

def is_person_award(award_name):
  people_words = ['actress','actor', 'director']
  return any([ word in award_name for word in people_words ])

DEAD_WORDS = [ 'performance', 'best', 'role', 'made', 'television']

def award_to_query(award_name):
  document = nlp_spacy(award_name)
  
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct or token.text in DEAD_WORDS) ]
  arr = list(set(arr))
  query = ' '.join([ '"' + s + '"' for s in arr ])

  return query
