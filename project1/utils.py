import re

# Combine entities of the same type that are right next to each other in text
# This lets us get full names and movies/shows with multiple names
# entities is a list of tuples of (string, type-of-entity)
# entity_type is the type that we are looking to combine
def getNamesAndCombineAdjacentEntities(entities, entity_type):
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

def getEntities(text, entity, nlp):
  # nlp should be Stanford CoreNLP pipeline so we can use 
  # named entity recongition to tag all the words
  tagged_words = nlp.ner(text)
  entities = getNamesAndCombineAdjacentEntities(tagged_words, entity)
  return entities

# Using regular expressions to clean a tweet's text
# Removes hashtags, @mentions, urls, and retweet tag 'RT'
# tweet is the text of a tweet
def clean_tweet(tweet):
  tweet = re.sub(r'#[a-zA-Z]+\b', '', tweet)
  tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
  tweet = re.sub(r'\bRT\b', '', tweet)
  return tweet

# To split a string into multiple strings of 10,000 characters so any one string isn't too large
def splitCount(s, count):
  return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]

# Flatten a list of sublists to be just a list
def flatten(lst):
  return [item for sublist in lst for item in sublist] 







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