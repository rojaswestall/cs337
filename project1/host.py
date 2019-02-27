import utils
from utils import safe_run_hosts

# We need to be passed the Stanford CoreNLP pipeline
@safe_run_hosts
def get_hosts(collection, nlp):
    host_tweets = collection.find({ "$text": { "$search": 'host -"next year"'}}) #1500
    corpus = utils.corpify_tweets(host_tweets)
    people = utils.get_people(corpus, nlp)
    winners = utils.choose_entities_over_threshold(people, 0.25)

    print(winners)
    return winners