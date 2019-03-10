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
from fractions import Fraction
import numpy as np
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

def pos_tag_ingredients(ing):
    ing_tokens = normalize_ingredients(ing)
    pos_tag_ing = nltk.pos_tag(ing_tokens)
    return pos_tag_ing


def get_phrases_from_chunks(chunk_gram, ing_pos):
    chunkParser = nltk.RegexpParser(chunk_gram)
    chunked = chunkParser.parse(ing_pos)
    matches = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        leaves_words = [ leaf[0] for leaf in subtree.leaves() ]
        phrase = ' '.join(leaves_words)
        matches.append(phrase)

    return matches


def get_ingredient_name(ing_tokens):
    return None


def get_descriptor(ing_tokens):
    return None

def get_preparation(ing_tokens):
    return None


def identify_number(element):
    # int
    try:
        anumber = int(element)
    except ValueError:
        try:
            anumber = float(element)
        except ValueError:
            try:
                anumber = float(Fraction(element))
            except ValueError:
                element = None
    return element


def parse_ingredients(ing_string):
    ''' 
    ------------------------------------------------------------------------ 
    input: a string of directions
    output: a dictionary
    ------------------------------------------------------------------------ 
    '''
    ing_pos_tags = pos_tag_ingredients(ing_string)
    #print(ing_pos_tags)
    # Get quantity
    quantity_chunker = r"""Chunk: {<CD>}"""  
    quantity_lst = get_phrases_from_chunks(quantity_chunker, ing_pos_tags)
    # make sure the quantity list contains all numeric values in string format
    quantity_lst = [element for element in quantity_lst if identify_number(element) is not None]
    print(quantity_lst)
    #print(quantity_lst)
    if not quantity_lst: 
        quantity = None
    elif len(quantity_lst) == 1:
        quantity = quantity_lst[0]
    else:
        quantity = quantity_lst[-1]
    #print(ing_string, quantity)

    # Measurement: knowledge base
    for_liquids = ['teaspoon', 'teaspoons', 'tablespoon', 'tablespoons', 'dessertspoon', 'dessertspoons', 'gallen', 'gallens', 'quart', 'quarts','bottle', 'bottles', 'cup', 'cups'] 
    for_solids = ['ounce', 'ounces', 'pound', 'pounds', 'slice', 'slices', 'inch', 'inches', 'stalk', 'stalks', 'bag', 'bags', 'packet', 'packets', 'package', 'packages', 'rib', 'ribs', 'clove', 'cloves', 'pinch', 'pinches', 'piece', 'pieces', 'can', 'cans', 'bag', 'bags']
    quantity_measurements = for_liquids + for_solids

    # create two lists by text and pos-tags
    text_ls, tag_ls = map(list, zip(*ing_pos_tags))
    if not quantity:
        measurement = None
    else:
        # in case there are two same number
        q_i = [i for i, text in enumerate(text_ls) if text in (quantity_lst)]
        print(q_i)
        m_i = [i + 1 for i in q_i]
        m_maybe = np.array(text_ls)[m_i]
        print(m_maybe)
        measurement_lst = [element for element in m_maybe if element in quantity_measurements]
        if len(measurement_lst) == 1:
            measurement = measurement_lst[0]
        else:
            measurement = None

    # once identified q and m, remove all q and m relevant words
    text_ls = [text for text in text_ls if text not in quantity_lst + quantity_measurements]
    print(ing_string)
    print(quantity, measurement)
    print(text_ls)
    print()
        
    # get ingredient name
    # the last NN or NNS in the tokenized list is the ingredient
#    NN_index = [i for i, tag in enumerate(tag_ls) if tag == 'NN' or tag == 'NNS']
#    ingredient = text_ls[NN_index[-1]]
#    print(ingredient)

    
    # create the output dictionary 
#    output_dict = {'ingredient': ingredient,
#                   'quantity': quantity,
#                   'measurement': measurement,
#                   'descriptor': descriptor,
#                   'preparation': preparation}

#    return output_dict


# test trial
#print('1 cup white sugar')
#get_ingredients('1 cup white sugar')

#print('1 cup chopped walnuts')
#get_ingredients('1 cup chopped walnuts')

#print('2 teaspoons hot water')
#get_ingredients('2 teaspoons hot water')

#print('1 teaspoon baking soda')
#get_ingredients('1 teaspoon baking soda')

# this trial has bug...
#print('2 eggs')
#get_ingredients('2 eggs')
