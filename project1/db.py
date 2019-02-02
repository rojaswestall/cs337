from pymongo import MongoClient
import pymongo
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint

# Run bash script for mongo setup ...

client = MongoClient()

db = client['gg-twitter']

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

    lists_of_tuples = [tree.leaves() for tree in subtrees]
    def fun(x):
        y = [ t[0] for t in x  ]
        z = ' '.join(y)
        return z

    people = [ fun(x) for x in lists_of_tuples ]
    return people


host_dict = {}
host_tweets = db['gg2013'].find({ "$text": { "$search": "host hosts"}})

# tweet = db['gg2013'].find_one({"id": 290634374695763968})

for i, doc in enumerate(host_tweets): 
    people = names_from_tweet(doc)
    for name in people:
        if name in host_dict:
            host_dict[name] += 1
        else:
            host_dict[name] = 1

gg = sorted(host_dict.items(), key=lambda x: x[1])
print(gg)

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