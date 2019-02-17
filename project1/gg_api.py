'''Version 0.35'''
import award_people
import host
import json
import pymongo
import atexit
from stanfordcorenlp import StanfordCoreNLP

# Connect to the Mongo Client
client = pymongo.MongoClient()

# Open the config file and set the correct db and collection
f = open('config.json')
CONFIG = json.load(f)
db = client[CONFIG["dbName"]]
f.close()

# Open the Stanford CoreNLP Pipeline
nlp = StanfordCoreNLP('http://localhost', port=9000)

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

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = host.get_hosts(collection(year), nlp)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = []
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
            count = c.count_documents({})
            print(year, count)

    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # years = ['2013','2015','2018','2019']
    years = ['2013']
    
    yearly_results = { year: 
            { award: award_people.process_award(award, collection(year), nlp) for award in OFFICIAL_AWARDS_1315 }
        for year in years }

    answers = { year: {
        'winners': { award: result[0] for award, result in results.items() },
        'nominees': { award: result[1] for award, result in results.items() },
        'presenters': { award: result[2] for award, result in results.items() },
    } for year, results in yearly_results.items() }

    json_str = json.dumps(answers)
    with open(CONFIG['pathToAnswers'], 'w+') as f:
        f.write(json_str)

    return

def exit_handler():
    nlp.close()

atexit.register(exit_handler)

if __name__ == '__main__':
    main()
