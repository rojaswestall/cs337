from pymongo import MongoClient
import pymongo
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
# import "./config.json" as config
import json

# Run bash script for mongo setup ...

client = MongoClient()

f = open('config.json')
data = json.load(f)
collection = data["dbCollection"]
db = client[data["dbName"]]
f.close()


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


host_dict = {}
host_tweets = db[collection].find({ "$text": { "$search": 'host hosts -"next year"'}})

# tweet = db['gg2013'].find_one({"id": 290634374695763968})
count = 0
for i, doc in enumerate(host_tweets):
    people = names_from_tweet(doc)
    for name in people:
        count += 1
        if name in host_dict:
            host_dict[name] += 1
        else:
            host_dict[name] = 1

gg = list(reversed(sorted(host_dict.items(), key=lambda x: x[1])))

for i, name in enumerate(gg):
    if i > 5: break
    print(name)

# Check correlation on the first two potential hosts
# If no correlation return the top result
# If there is correlation, try again with the third result
correlation_tweets = db[collection].find({ "$text": { "$search": 'host hosts -"next year" "'  + gg[0][0] + '" "' + gg[1][0] + '"'}})

#  Now compare this to the number that is returned in gg


print("sum of name counts: ", count)

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