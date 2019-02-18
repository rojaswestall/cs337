import pymongo
import utils

# We need to be passed the Stanford CoreNLP pipeline
def get_hosts(collection, nlp):
    host_tweets = collection.find({ "$text": { "$search": 'host -"next year"'}}).limit(1500)
    corpus = utils.corpify_tweets(host_tweets)
    people = utils.get_people(corpus, nlp)
    winners = utils.choose_entities_over_threshold(people)

    print(winners)
    return winners