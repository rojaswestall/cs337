import pymongo
from collections import Counter
import json
import atexit
import utils

# We need to be passed the Stanford CoreNLP pipeline
def getHosts(collection, nlp):
    host_tweets = collection.find({ "$text": { "$search": 'host hosts -"next year"'}})
    tweets_text = ' '.join([ tweet['text'] for tweet in host_tweets ])
    clean_text = utils.clean_tweet(tweets_text)
    documents = utils.splitCount(clean_text, 10000)
    winners = topPeople(documents, nlp)

    print(winners)
    return winners

def topPeople(docs, nlp):
    lst_of_lst_of_people = [ utils.getEntities(doc, 'PERSON', nlp) for doc in docs ]
    all_people = utils.flatten(lst_of_lst_of_people)
    
    # Use counter to get the top results
    c = Counter(all_people)
    # Pass it 2, assuming there will always be two hosts
    top_results = c.most_common(2)

    # In an attempt to correct tweets only using first names to refer to winners
    # we will take all results that have one word and add their count to the
    # result with one word or more with the largest count that also contains that word 

    print(c.most_common(5))

    if top_results:
        return [ result[0] for result in top_results ]
    else:
        return None  

