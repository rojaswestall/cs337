from pymongo import MongoClient
import utils
import json
import spacy

nlp = spacy.load('en')

# Connect to the Mongo Client
client = MongoClient()

# Open the config file and set the correct db and collection
f = open('config.json')
data = json.load(f)
collection = data["dbCollections"]["2013"]
db = client[data["dbName"]]
f.close()

# We need to be passed the Stanford CoreNLP pipeline
def get_worst_dressed(collection, nlp):
    worst_dressed_tweets = collection.find({ "$text": { "$search": '"dress" awful hate wtf worst ugly terrible -RT -tina -gorgeous -stunning -beautiful' } }).limit(2000)
    corpus = utils.corpify_tweets(worst_dressed_tweets)
    people = utils.get_people(corpus, nlp)
    worst_dressed = utils.choose_best_entities(people, 5)

    print(worst_dressed)
    return worst_dressed

# get_worst_dressed(db['gg2013'], nlp)
