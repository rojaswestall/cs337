# Project 1 - Twitter

- Install python 3.7 (they might use 3.6)
- Install mongodb (follow their instructions)
- run `mongod` in one terminal
- Open another terminal and run setup.sh to make db with data. Make sure gg2013.json and gg2015.json are in the project1 folder in order to make the mongodb
- `setup.sh` calls mongo sript
- mongo script imports data and creates index



1. Build a MongoDB to facilitate data analysis
2. How to get a full list of awards, artists, and films.
3. Data cleaning
	- Assign tweets into different blocks and check each block separately to test reliability?
	- Data cleaning: identify and label important tweets for each question as it is unfeasible to process 2M tweets so better narrow it down and find relevant and important tweets to tackle each question.
		> @mention: keep specific @mention while removing everything else
		> url: remove all 
		> emoji: keep specific emojis (trophies, peace)
		> length: discard tweets below certain length after removing all unnecessary contents
		> retweets: tweets got the most retweets have higher importance?


Gabe Ideas:
- We might get multiple names for an award. We can keep track of the different winners/nominees by award and keep a count for each of the names


Minimum requirement questions:
1. Find host name? 
	- Get all twitter handles from the dataset and create a separate table map handles to real users
	- Get all tweets that have the keyword “Host” and get all names from those tweets. Calculate the max occurrence of names and take that as our answer to the question.

2. Award names

3. Presenters, mapped to awards

4. Nominees, mapped to awards

5. Winnters, mapped to awards



Resources we used:
- [nltk libraries and examples](https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da?fbclid=IwAR0m3EPkwcjTnqWJvxN-HKlGImYFY3X2yi7DjJKe0lHJVKpiYQK6tZidPZY)