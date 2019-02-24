from pymongo import MongoClient
import utils
import atexit
import json
from stanfordcorenlp import StanfordCoreNLP

# Connect to the Mongo Client
client = MongoClient()

# Open the config file and set the correct db and collection
f = open('config.json')
data = json.load(f)
collection = data["dbCollections"]["2013"]
db = client[data["dbName"]]
f.close()

# Open the Stanford CoreNLP Pipeline
nlp = StanfordCoreNLP('http://localhost', port=9000)

# We need to be passed the Stanford CoreNLP pipeline
def get_best_dressed(collection, nlp):
    best_dressed_tweets = collection.find({ "$text": { "$search": '"look" love stunning gorgeous -RT -tina -ugly -awful'} }).limit(2000)
    corpus = utils.corpify_tweets(best_dressed_tweets)
    people = utils.get_people(corpus, nlp)
    best_dressed = utils.choose_best_entities(people, 5)

    print(best_dressed)
    return best_dressed

def exit_handler():
    nlp.close()

atexit.register(exit_handler)

# get_best_dressed(db['gg2013'], nlp)
