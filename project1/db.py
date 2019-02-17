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
import re

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
# categories = ["best drama", "best comedy or musical", "best screenplay", "best director", "best actor in a drama", "best actress in drama", "best actor in a comedy or musical", "best actress in a comedy or musical", "best supporting actress", "best supporting actor", "best foreign film", "best animation", "best original score", "best original song", "best television drama", "best actress, TV drama", "best actor, TV drama", "best comedy", "best actress, comedy", "best actor, comedy", "best TV movie or miniseries", "best actress, mini series or musical", "best actor, miniseries of TV movie", "best supporting actress", "best supporting actor", "Cecil B DeMille award"]
# categories_without_best = ["drama", "comedy or musical", "screenplay", "director", "actor in a drama", "actress in drama", "actor in a comedy or musical", "actress in a comedy or musical", "supporting actress", "supporting actor", "foreign film", "animation", "original score", "original song", "television drama", "actress, TV drama", "actor, TV drama", "comedy", "actress, comedy", "actor, comedy", "TV movie or miniseries", "actress, mini series or musical", "actor, miniseries of TV movie", "supporting actress", "supporting actor", "Cecil B DeMille award"]

##### ACCORDING TO THE TAs #####
OFFICIAL_AWARDS_1315 = [
    'cecil b. demille award', 
    'best motion picture - drama', 
    'best performance by an actress in a motion picture - drama', 
    'best performance by an actor in a motion picture - drama', 
    'best motion picture - comedy or musical', 
    'best performance by an actress in a motion picture - comedy or musical', 
    'best performance by an actor in a motion picture - comedy or musical', 
    'best animated feature film', 
    'best foreign language film', 
    'best performance by an actress in a supporting role in a motion picture', 
    'best performance by an actor in a supporting role in a motion picture', 
    'best director - motion picture', 
    'best screenplay - motion picture', 
    'best original score - motion picture', 
    'best original song - motion picture', 
    'best television series - drama', 
    'best performance by an actress in a television series - drama', 
    'best performance by an actor in a television series - drama', 
    'best television series - comedy or musical', 
    'best performance by an actress in a television series - comedy or musical', 
    'best performance by an actor in a television series - comedy or musical', 
    'best mini-series or motion picture made for television', 
    'best performance by an actress in a mini-series or motion picture made for television', 
    'best performance by an actor in a mini-series or motion picture made for television', 
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


# host_tweets = db[collection].find({ "$text": { "$search": 'host hosts -"next year"'}})

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

def does_contain(words, word):


for i, result in enumerate(top_results):
    for j in range(0,i):
        result[0]