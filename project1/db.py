from pymongo import MongoClient

# Run bash script for mongo setup ...

client = MongoClient()

db = client['test-database']