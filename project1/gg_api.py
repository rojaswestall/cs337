'''Version 0.35'''
import award_people
import award_names
import host
import bestdressed
import worstdressed
import json
from pymongo import MongoClient
import pymongo
import spacy

nlp = spacy.load('en')

# Connect to the Mongo Client
client = MongoClient()

# Open the config file and set the correct db and collection
f = open('config.json')
CONFIG = json.load(f)
db = client[CONFIG["dbName"]]
f.close()

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def collection(year):
    c = CONFIG["dbCollections"][year]
    return db[c]

def read_answers(year, key):
    try:
        with open(CONFIG['pathToAnswers']) as f:
            winners = json.load(f)[year][key]
            return winners
    except:
        return { award: '' for award in OFFICIAL_AWARDS_1315 }

def award_list(year):
    if year == '2013' or year == '2015':
        return OFFICIAL_AWARDS_1315
    elif year == '2018' or year == '2019':
        return OFFICIAL_AWARDS_1819

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = read_answers(year, 'hosts')
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = read_answers(year, 'awards')
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return read_answers(year, 'nominees')

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return read_answers(year, 'winners')

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return read_answers(year, 'presenters')

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

    for year, filepath in CONFIG['pathToTweets'].items():

        with open(filepath) as tweets_json:
            tweets_python = json.load(tweets_json)
            c = collection(year)
            c.insert_many(tweets_python)
            c.create_index([('text', pymongo.TEXT)])

    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    years = ['2013','2015','2018','2019']

    awards = { year: award_names.award_names(collection(year), nlp) for year in years }
    hosts = { year: host.get_hosts(collection(year), nlp) for year in years }

    yearly_results = { year: 
            {  award: award_people.process_award(award, hosts[year], collection(year), nlp) for award in award_list(year) }
        for year in years }

    answers = { year: {
        'hosts': hosts[year],
        'winners': { award: result[0] for award, result in results.items() },
        'nominees': { award: result[1] for award, result in results.items() },
        'presenters': { award: result[2] for award, result in results.items() },
        'awards': awards[year]
    } for year, results in yearly_results.items() }

    json_str = json.dumps(answers)

    with open(CONFIG['pathToAnswers'], 'w+') as f:
        f.write(json_str)


    return

if __name__ == '__main__':
    main()
