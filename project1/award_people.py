import spacy
import pymongo
from collections import Counter
import utils

nlp_spacy = spacy.load('en')

BUCKET_SIZE_SEC = 50 
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

RELEVANT_TWEETS_LIMIT = 1000

def process_award(award_name, hosts, db_collection, nlp):
  print('\n\n', award_name.upper())
  peak_timestamp = find_peak_activity(award_name, db_collection)
  if not peak_timestamp: return '' , '', ''

  print('\nwinner')
  winner = find_winner(award_name, peak_timestamp, db_collection, nlp)

  print('\npresenters')
  other_people = [ winner ] + hosts
  presenters = find_presenters(award_name, peak_timestamp, other_people, db_collection, nlp)

  print('\nnominees')
  other_people = presenters + [ winner ] + hosts
  nominees = find_nominees(award_name, other_people, peak_timestamp, db_collection, nlp)

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
  winner = utils.choose_n_best_entities(entities, 1)[0]
  return winner

def find_nominees(award_name, other_people, peak_timestamp, db_collection, nlp):
  interval = get_relevant_interval(peak_timestamp, 0, 1)
  query_str = ' '.join([ utils.minus(person) for person in other_people ])
  print('q', query_str)
  tweets = relevant_tweets(interval, 'rob snub won wish ' + query_str , db_collection)
  corpus = utils.corpify_tweets(tweets)

  entities = utils.get_people(corpus, nlp) if is_person_award(award_name) else get_proper_nouns(corpus, nlp)
  # names = [ name for name in entities if name not in other_people ]
  nominees = utils.choose_n_best_entities(entities, 4)
  return nominees

# def prune_names(entities, other_people):
#   return [ name for name in entities if name not in other_people ]

def find_presenters(award_name, peak_timestamp, other_people, db_collection, nlp):
  interval = get_relevant_interval(peak_timestamp, 1, 0)
  query_str = ' '.join([ utils.minus(person) for person in other_people ])
  query_str += ' ' + award_to_soft_query(award_name)
  query_str += ' presents presenters introduces intros introducing announce announcing announcers -"surprise"'
  print('query: ', query_str, '\npeak_lt: ', interval[1], '\npeak_gt: ', interval[0]) 
  tweets = relevant_tweets(interval, query_str, db_collection)
  corpus = utils.corpify_tweets(tweets)
  entities = utils.get_people(corpus, nlp)
  winner = utils.choose_n_best_entities(entities, 2)
  return winner

def get_relevant_interval(peak, negative_width, positive_width):
  interval = [ 
    peak-(negative_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS),
    peak+(positive_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS), 
    ]
  print(interval)
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

def award_to_soft_query(award_name):
  document = nlp_spacy(award_name)
  
  arr = [ token.text for token in document if not (token.is_stop or token.is_punct or token.text in DEAD_WORDS) ]
  arr = list(set(arr))
  query = ' '.join([ s for s in arr ])

  return query

