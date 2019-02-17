import pymongo
import utils

# We need to be passed the Stanford CoreNLP pipeline
def get_hosts(collection, nlp):
    host_tweets = collection.find({ "$text": { "$search": 'host -"next year"'}}).limit(2000)
    corpus = utils.corpify_tweets(host_tweets)
    people = utils.get_people(corpus, nlp)
    winners = utils.choose_best_entities(people, 2)

    print(winners)
    return winners
