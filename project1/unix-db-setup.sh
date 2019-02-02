#!/bin/sh
DB_NAME=$( jq -r '.dbName' config.json)
PATH_TO_TWEETS=$( jq -r '.pathToTweets' config.json )
DB_COLLECTION=$( jq -r '.dbCollection' config.json )
# echo $DB_NAME
# echo $PATH_TO_TWEETS
# echo $DB_COLLECTION
mongoimport --db $DB_NAME --collection $DB_COLLECTION --file $PATH_TO_TWEETS --jsonArray
mongo db-setup.js
