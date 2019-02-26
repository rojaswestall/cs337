# Project 1 - Twitter

Gabriel Rojas-Westall, Jeff Holm, David Latimore II, Dongping

## What to Install

### MongoDB

Instructions for downloading and installing MongoDB can be found [here](https://docs.mongodb.com/manual/installation/).

### Stanford CoreNLP

Download version 3.9.1 of the [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/history.html) library. The version is important so we can use a python wrapper with it. The latest version of the Stanford CoreNLP library is 3.9.2 so the python wrapper is very up to date regardless.

To use the Stanford CoreNLP library with Python:
`pip install stanfordcorenlp`

### Spacy

To install Spacy, simply run `python3 -m spacy download en`

### NTLK

To install NLTK, run `sudo pip install -U nltk`. You may be prompted for an administrator's password to complete this installation step.

## How to run our project

In order to get this project to run, you'll need Stanford CoreNLP, NLTK, MongoDB, and Spacy installed. After you've installed those technologies, you can do the following to run our project:

- Run `mongod` in one terminal
- In a second terminal, start the Stanford CoreNLP Server by `cd`-ing into the Stanford CoreNLP directory (which you should have downloaded) earlier and running one of the two commands
  - `java -mx4g -cp "*" --add-modules java.se.ee edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000`
  - `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000`
- In a third terminal window, call `python gg_api.py` to run our main function.

## Resources used and Papers referenced

### Papers

This paper uses Twitter data to predict the box office revenue with the assumption that movies that are well talked about are well watched. So we borrowed and modified their assumptions that  “artists who are well talked about are more likely to win”. This paper also introduces us to start thinking about how to relate tweets associated with time.
[Asur, S., & Huberman, B. A. (2010, August). Predicting the future with social media. In Proceedings of the 2010 IEEE/WIC/ACM International Conference on Web Intelligence and Intelligent Agent Technology-Volume 01 (pp. 492-499). IEEE Computer Society.](https://arxiv.org/pdf/1003.5699.pdf)

Leskovec et al. shows the temporal dynamics of the most popular topics in social media are indeed made up of a succession of rising and falling patterns of popularity, in other words, successive bursts of popularity.
[Leskovec, J., Backstrom, L., & Kleinberg, J. (2009, June). Meme-tracking and the dynamics of the news cycle. In Proceedings of the 15th ACM SIGKDD international conference on Knowledge discovery and data mining (pp. 497-506). ACM.](http://www.freelanceunbound.com/wp-content/uploads/2009/09/quotes-kdd09.pdf)

Shamma et al. propose a simple model, PT (i.e. Peaky Topics) , similar to the classical tf-idf model [44] in the sense that it is based on a normalized term frequency metric. So we group tweets in specific time intervals and study them as a pseudo-document.
[Shamma, D. A., Kennedy, L., & Churchill, E. F. (2011, March). Peaks and persistence: modeling the shape of microblog conversations. In Proceedings of the ACM 2011 conference on Computer supported cooperative work (pp. 355-358). ACM.](https://www.researchgate.net/profile/Elizabeth_Churchill/publication/220879043_Peaks_and_persistence_modeling_the_shape_of_microblog_conversations/links/0912f50c61981c1278000000/Peaks-and-persistence-modeling-the-shape-of-microblog-conversations.pdf)

Parts of this paper is a nice methodological summary and survey of current method relating to topic modeling on social media data.
[Guille, A., Hacid, H., Favre, C., & Zighed, D. A. (2013). Information diffusion in online social networks: A survey. ACM Sigmod Record, 42(2), 17-28.](https://hal.archives-ouvertes.fr/hal-00848050/document)

This paper shows the performance of standard NLP tools is severely degraded on tweets. So we were searching different NER tools, and discovered Stanford CoreNLP.
[Ritter, A., Clark, S., & Etzioni, O. (2011, July). Named entity recognition in tweets: an experimental study. In Proceedings of the conference on empirical methods in natural language processing (pp. 1524-1534). Association for Computational Linguistics.](http://www.aclweb.org/anthology/D11-1141)

### Other Resources

- [nltk libraries and examples](https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da?fbclid=IwAR0m3EPkwcjTnqWJvxN-HKlGImYFY3X2yi7DjJKe0lHJVKpiYQK6tZidPZY)
- [PyMongo Documentation](https://api.mongodb.com/python/current/) for mongo with python
- [MongoDB Documentation](https://docs.mongodb.com/manual/tutorial/query-documents/) mostly for use with compass
- Stack Overflow for genral python help
