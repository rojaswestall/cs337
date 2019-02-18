import pymongo
from collections import Counter
import utils
from nltk.tokenize import word_tokenize


BUCKET_SIZE_SEC = 50
BUCKET_SIZE_MS = BUCKET_SIZE_SEC * 1000
BUCKETS_IN_INTERVAL = 3

RELEVANT_TWEETS_LIMIT = 800

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
  query_str = utils.award_to_query(award_name)
  print('qp',query_str)
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

  entities = utils.get_people(corpus, nlp) if utils.is_person_award(award_name) else get_proper_nouns(corpus, nlp)

  winner = utils.choose_best_entities(entities, 1)[0]
  # if award_name == 'best television series - comedy or musical':
  #   print('heyo')
  #   print (interval)
  #   print(entities)
  return winner

def find_nominees(award_name, other_people, peak_timestamp, db_collection, nlp):
  interval = get_relevant_interval(peak_timestamp, 1, 1)
  query_str = ' '.join([ utils.minus(person) for person in other_people ])
  tweets = relevant_tweets(interval, 'hope rob snub won win wish ' + query_str , db_collection)

  corpus = utils.corpify_tweets(tweets)

  entities = utils.get_people(corpus, nlp) if utils.is_person_award(award_name) else get_proper_nouns(corpus, nlp)
  nominees = utils.choose_entities_over_threshold(entities)
  return nominees

def find_presenters(award_name, peak_timestamp, other_people, db_collection, nlp):
  interval = get_relevant_interval(peak_timestamp, 1, 0)
  query_str = ' '.join([ utils.minus(person) for person in other_people ])
  query_str += ' ' + utils.award_to_soft_query(award_name)
  query_str += ' presents presenters introduces intros introducing announce announcing announcers -"surprise"'
  # print('query: ', query_str, '\npeak_lt: ', interval[1], '\npeak_gt: ', interval[0])
  tweets = relevant_tweets(interval, query_str, db_collection)
  corpus = utils.corpify_tweets(tweets)
  entities = utils.get_people(corpus, nlp)

  presenters = utils.choose_entities_over_threshold(entities)
  return presenters

def get_relevant_interval(peak, negative_width, positive_width):
  interval = [
    peak-(negative_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS),
    peak+(positive_width*BUCKETS_IN_INTERVAL*BUCKET_SIZE_MS),
    ]
  # print(interval)
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

def award_to_query(award_name): #Removes all stop words. Returns
    # stop_words = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}

    word_tokens = word_tokenize(award_name)
    filtered_sentence = [w for w in word_tokens if not w in DEAD_WORDS]
    filtered_sentence = list(set(filtered_sentence))
    query = ' '.join([ '"' + s + '"' for s in filtered_sentence ])

    return query
