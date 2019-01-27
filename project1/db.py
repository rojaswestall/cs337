from pymongo import MongoClient
import pymongo

# Run bash script for mongo setup ...

client = MongoClient()

db = client['gg-twitter']

# tweets2015 = db['tweets-2015'].find_one({"text": 554403687448469504})

db['tweets-2015'].create_index([("text", pymongo.TEXT)])

tweets2015 = db['tweets-2015'].find({ "$text": { "$search": "host golden globes"}})

for i, doc in enumerate(tweets2015):
	if i > 10: break
	print(doc)

print(tweets2015)

# tweets-2015 is collection