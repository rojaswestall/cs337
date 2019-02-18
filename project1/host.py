import pymongo
import utils
from utils import safe_run_hosts

# We need to be passed the Stanford CoreNLP pipeline
@safe_run_hosts
def get_hosts(collection, nlp):
    host_tweets = collection.find({ "$text": { "$search": 'host -"next year"'}}).limit(1500) #1500
    corpus = utils.corpify_tweets(host_tweets)
    people = utils.get_people(corpus, nlp)
    winners = utils.choose_entities_over_threshold(people)

    print(winners)
    return winners