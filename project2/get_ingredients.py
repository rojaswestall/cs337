# input "1 cup white sugar"
# output
    # ingredient: sugar
    # quantity: 1
    # measurement: cup
    # descriptior: white
    # preparation: ''

# input "1 cup butter, softened"
# output
    # ingredient: butter
    # quantity: 1
    # measurement: cup
    # descriptior: ''
    # preparation: 'soften'

import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

def clean_ingredients(ing):
    # basic cleaning
        # remove all punctiation
        # keep / : 1/5 pounds
        # keep . : 1.5 pounds
    pattern = '[,;!$%^&*()]'
    ing = ' '.join(re.sub(pattern," ",ing).split())
    return ing


def normalize_ingredients(ing):
    ing = clean_ingredients(ing)
    # convert all words to lower case
    ing_lower = ing.lower()
    # tokenize all tweet text
    ing_tokens = nltk.word_tokenize(ing_lower)

    # default nltk stop words
    stop_words_nltk = stopwords.words('english')
    # remove English stop words based on default nltk package
    ing_normalized_text = [word for word in ing_tokens if word not in stop_words_nltk]

    return ing_normalized_text


def get_phrases_from_chunks(chunk_gram, ing_pos):
    chunkParser = nltk.RegexpParser(chunk_gram)
    chunked = chunkParser.parse(ing_pos)
    matches = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        leaves_words = [ leaf[0] for leaf in subtree.leaves() ]
        phrase = ' '.join(leaves_words)
        matches.append(phrase)

    return matches


def get_ingredients(ing_string):
    ''' 
    ------------------------------------------------------------------------ 
    input: a string of directions
    output: a dictionary
    ------------------------------------------------------------------------ 
    '''
    # normalize ingredients
    ing_tokens = normalize_ingredients(ing_string)
    # pos tagging tweet tokens
    ing_pos_tags = nltk.pos_tag(ing_tokens)

    # chunking: quantity which is a numeric number
    quantity_chunker = r"""Chunk: {<CD>}"""  
    quantity = get_phrases_from_chunks(quantity_chunker, ing_pos_tags)[0]
    print(quantity)

    # chunking: measurement
    # if the first tag is CD (a quantity), the second NN or NNS is the measurement
    text_ls, tag_ls = map(list, zip(*ing_pos_tags))
    if tag_ls[0] == 'CD':
        measurement = text_ls[1]
    print(measurement)
        
    # get ingredient name
    # the last NN or NNS in the tokenized list is the ingredient
    NN_index = [i for i, tag in enumerate(tag_ls) if tag == 'NN' or tag == 'NNS']
    ingredient = text_ls[NN_index[-1]]
    print(ingredient)
    
    # create the output dictionary 
    output_dict = {'ingredient': ingredient,
                   'quantity': quantity,
                   'measurement': measurement}

    return output_dict


# test trial
print('1 cup white sugar')
get_ingredients('1 cup white sugar')

print('1 cup chopped walnuts')
get_ingredients('1 cup chopped walnuts')

print('2 teaspoons hot water')
get_ingredients('2 teaspoons hot water')

print('1 teaspoon baking soda')
get_ingredients('1 teaspoon baking soda')

# this trial has bug...
print('2 eggs')
get_ingredients('2 eggs')
