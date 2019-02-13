from pymongo import MongoClient
import pymongo
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import json
import datetime
import time

# Before running this, the bash script should be run for whatever year you want to run the script for
# This bash script will setup mongo for that year

# Connect to the Mongo Client
client = MongoClient()

# Open the config file and set the correct db and collection
f = open('config.json')
data = json.load(f)
collection = data["dbCollection"]
db = client[data["dbName"]]
f.close()



# RANDOM CODE TO HELP US:

# FIND ONE ITEM IN THE DB
# tweets2015 = db['tweets-2015'].find_one({"id": 554403687448469504})
# print(tweets2015)

# CREATE AN INDEX SHOULD BE DONE BEFORE RUNNING MAIN SCRIPT
# db['tweets-2015'].create_index([("text", pymongo.TEXT)])

# SEARCH THE TEXT INDEX THAT WE MADE WITH CERTAIN SEARCH PARAMS
# tweets2015 = db['tweets-2015'].find({ "$text": { "$search": "host golden globes"}})
# for i, doc in enumerate(tweets2015):
# 	if i > 10: break
# 	print(doc)

# IN COMPASS filter bar
# { $text: { $search: 'host'} }



# Just for ourselves to test:
categories = ["best drama", "best comedy or musical", "best screenplay", "best director", "best actor in a drama", "best actress in drama", "best actor in a comedy or musical", "best actress in a comedy or musical", "best supporting actress", "best supporting actor", "best foreign film", "best animation", "best original score", "best original song", "best television drama", "best actress, TV drama", "best actor, TV drama", "best comedy", "best actress, comedy", "best actor, comedy", "best TV movie or miniseries", "best actress, mini series or musical", "best actor, miniseries of TV movie", "best supporting actress", "best supporting actor", "Cecil B DeMille award"]
categories_without_best = ["drama", "comedy or musical", "screenplay", "director", "actor in a drama", "actress in drama", "actor in a comedy or musical", "actress in a comedy or musical", "supporting actress", "supporting actor", "foreign film", "animation", "original score", "original song", "television drama", "actress, TV drama", "actor, TV drama", "comedy", "actress, comedy", "actor, comedy", "TV movie or miniseries", "actress, mini series or musical", "actor, miniseries of TV movie", "supporting actress", "supporting actor", "Cecil B DeMille award"]

host_tweets = db[collection].find({ "$text": { "$search": 'host hosts -"next year"'}})

# Keep track of all the proper nouns and return the ones with a certain percentage more than the total number of tweets
def names_from_tweet(tweet):
    ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(tweet['text'])))
    subtrees = filter(lambda x: x.label() == 'PERSON', ne_tree.subtrees())
    full_name_trees = filter(lambda x: len(x.leaves()) >= 2, subtrees)
    lists_of_tuples = [tree.leaves() for tree in full_name_trees]
    def fun(x):
        y = [ t[0] for t in x  ]
        z = ' '.join(y)
        return z

    people = [ fun(x) for x in lists_of_tuples ]
    return people

def getNamesFromSearch(cursor):
    name_dict = {}
    count = 0
    for i, doc in enumerate(cursor):
        people = names_from_tweet(doc)
        for name in people:
            count += 1
            if name in name_dict:
                name_dict[name] += 1
            else:
                name_dict[name] = 1
    return name_dict

def createCategorySearchString(category):
    return '"' + category + '"'
    # + 'win winner won wins best congratulations congrats 🎉 🎊 🏆 🎬 🎤 🎞 📽 🎥'

def getBestFromDict(dct):
    return list(reversed(sorted(dct.items(), key=lambda x: x[1])))

# host_dict = getNamesFromSearch(host_tweets)
# gg = getBestFromDict(host_dict)
# print("hosts results: \n")
# for i, name in enumerate(gg):
#     if i > 5: break
#     print(name)
# print("\n\n")

# for category in categories_without_best:
#     tweets = db[collection].find({ "$text": { "$search": createCategorySearchString(category)}})
#     dic = getNamesFromSearch(tweets)
#     best = getBestFromDict(dic)
#     print(category + ": \n")
#     for i, name in enumerate(best):
#         if i > 5: break
#         print(name)
#     print("\n\n")


def sortByTime(cursor):
    time_dict = {}
    for i, tweet in enumerate(cursor):
        tm = tweet['timestamp_ms']
        # Only care about the 100 second period so use -6
        shortened = str(tm)[:-5]
        if shortened in time_dict:
            time_dict[shortened] +=1
        else:
            time_dict[shortened] = 1
    return time_dict


tweets = db[collection].find({ "$text": { "$search": '"drama"'}})
dic = sortByTime(tweets)
for key, value in sorted(dic.items()):
    epoch = datetime.datetime.fromtimestamp(int(key + "00000")/1000.0)
    readable = epoch.strftime('%I:%M:%S')
    print(readable, ": ", value)













# Check correlation on the first two potential hosts
# If no correlation return the top result
# If there is correlation, try again with the third result
# correlation_tweets = db[collection].find({ "$text": { "$search": 'host hosts -"next year" "'  + gg[0][0] + '" "' + gg[1][0] + '"'}})

#  Now compare this to the number that is returned in gg


# print("sum of name counts: ", count)

# def preprocess(phrase):
#     tokenized = nltk.word_tokenize(phrase)
#     tokenized_and_tagged = nltk.pos_tag(tokenized)
#     return tokenized_and_tagged
    


# pptweet = preprocess(tweet['text'])
# print(pptweet)

# pattern = 'NP: {<DT>?<JJ>*<NN>}'

# cp = nltk.RegexpParser(pattern)
# cs = cp.parse(pptweet)
# print(cs)

# iob_tagged = tree2conlltags(cs)
# pprint(iob_tagged)


# Unrelated to above shit

# for tree in ne_tree.subtrees():
#     print(tree)
#     print(tree.label())
#     print(tree.leaves())


# tweets-2015 is collection