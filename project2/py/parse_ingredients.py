import re
import nltk
from nltk.corpus import stopwords
from fractions import Fraction
from ingredient import Ingredient
import utils


def clean_ingredients(ing):
    # basic cleaning
        # remove all punctiation
        # keep / : 1/5 pounds
        # keep . : 1.5 pounds
    pattern = '[,;!$%^&*]'
    ing = ' '.join(re.sub(pattern, " ", ing).split())
    return ing


def remove_allPunct(ing):
    pattern = '[.,;!$%^&*()/-]'
    ing = ' '.join(re.sub(pattern, " ", ing).split())
    return ing


def normalize_ingredients(ing):
    ing_lower = ing.lower()
    ing_tokens = nltk.word_tokenize(ing_lower)

    stop_words_nltk = stopwords.words('english')
    ing_normalized_text = [
        word for word in ing_tokens if word not in stop_words_nltk]

    return ing_normalized_text


def pos_tag_ingredients(normalized_tokens):
    pos_tag_ing = nltk.pos_tag(normalized_tokens)
    return pos_tag_ing


def get_phrases_from_chunks(chunk_gram, ing_pos):
    chunkParser = nltk.RegexpParser(chunk_gram)
    chunked = chunkParser.parse(ing_pos)
    matches = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        leaves_words = [leaf[0] for leaf in subtree.leaves()]
        phrase = ' '.join(leaves_words)
        matches.append(phrase)

    return matches


def identify_number(element):
    try:
        anumber = int(element)
    except ValueError:
        try:
            anumber = float(element)
        except ValueError:
            try:
                anumber = float(Fraction(element))
            except ValueError:
                anumber = None
    return anumber


def process_qm(lst):
    output_lst = []
    for element in lst:
        output_lst += element.split(' ')
    return output_lst


def parse_ingredients(ingredients, kb):
    ingredient_objs = [parse_ingredient(item, kb) for item in ingredients]
    return ingredient_objs


def parse_ingredient(ing_string, kb):
    '''
    ------------------------------------------------------------------------
    input: a string of ingredients
        - '2 tablespoons minced fresh ginger root'
    output: a dictionary
        {'text': '2 tablespoons minced fresh ginger root',
         'ingredient': 'ginger root',
         'quantity': '2',
         'measurement': 'tablespoons',
         'descriptor': 'fresh',
         'preparation': 'minced'}
    ------------------------------------------------------------------------
    '''
    # Measurement: knowledge base
    for_liquids = kb.liquid_measurements
    for_solids = kb.solid_measurements

    quantity_measurements = for_liquids + for_solids
    cleaned_string = clean_ingredients(ing_string)
    normalized_tokens = normalize_ingredients(cleaned_string)
    ing_pos_tags = pos_tag_ingredients(normalized_tokens)
    quantity_chunker = r"""Chunk: {<CD>{1,}<NN|NNS|JJ>}"""
    all_chunked_qm_lst = get_phrases_from_chunks(
        quantity_chunker, ing_pos_tags)

    if not all_chunked_qm_lst:
        qm = None
    else:
        qm = all_chunked_qm_lst[0]
    if qm is None:
        quantity = None
        measurement = None
    else:
        qm_lst = qm.split(' ')
        quantity_lst = []
        measurement_lst = []
        for element in qm_lst:
            if identify_number(element) is not None:
                quantity_lst.append(element)
            else:
                measurement_lst.append(element)

        quantity = ' '.join(quantity_lst)
        measurement = measurement_lst[0]

        if measurement not in quantity_measurements:
            measurement = None
    ##########################################################################
    ing_lower = ing_string.lower()
    # cut into
    p1 = re.compile('cut into .+')
    p_maybe = p1.findall(ing_lower)
    # remove everything in parentheses
    ing_lower = re.sub(r'\(.*\)', '', ing_lower)
    # remove everything followed by such as or e. g.
    ing_lower = ' '.join(re.sub("such as .+", " ", ing_lower).split())
    ing_lower = ' '.join(re.sub("e. g. .+", " ", ing_lower).split())
    ing_lower = ' '.join(re.sub("cut into .+", " ", ing_lower).split())
    # remove all puncts
    ing_nopunct = remove_allPunct(ing_lower)
    # normalization
    ing_tokens = normalize_ingredients(ing_nopunct)
    # remove all numbers
    ing_tokens = [x for x in ing_tokens if not any(c.isdigit() for c in x)]
    # remove all measurements
    ing_tokens = [x for x in ing_tokens if x not in quantity_measurements]
    ing_sstring = ' '.join(ing_tokens)
    ##########################################################################
    # Knowledge base: descriptor
    for_meat = kb.meat_descriptors
    for_veggie = kb.veggie_descriptors
    for_seafood = kb.seafood_descriptors
    for_seasoning = kb.seasoning_descriptors
    other = kb.other_descriptors

    ######## Is not used yet ########
    country_style = kb.style_descriptors
    # country_style = ['italian style', 'chinese style', 'swiss']
    #################################

    all_descriptor = for_meat + for_veggie + for_seafood + for_seasoning + country_style + other

    # Knowledge base: Preparation
    hard_prep = kb.hard_prep
    prep = kb.prep

    descriptor_lst = []
    for element in all_descriptor:
        if element in ing_sstring:
            descriptor_lst.append(element)
    if descriptor_lst != []:
        descriptor = ' and '.join(descriptor_lst)
    else:
        descriptor = None

    hard_prep_lst = []
    for element in hard_prep:
        if element in ing_sstring:
            hard_prep_lst.append(element)
    prep_lst = []
    for element in prep:
        if element in ing_sstring:
            prep_lst.append(element)

    for element1 in prep_lst:
        for element2 in hard_prep_lst:
            if element1 in element2:
                prep_lst.remove(element1)
    prep_lst += hard_prep_lst
    prep_lst = list(set(prep_lst))

    if prep_lst == [] and p_maybe != []:
        preparation = p_maybe[0]
    elif p_maybe != [] and not prep_lst:
        preparation = ' and '.join(prep_lst) + ' and ' + p_maybe[0]
    else:
        if prep_lst != []:
            preparation = ' and '.join(prep_lst)
        else:
            preparation = None

    # get ingredients
    remove_lst = prep_lst + descriptor_lst
    if remove_lst != []:
        for element in remove_lst:
            ing_sstring = re.sub(element, '', ing_sstring)
        ingredient = ing_sstring.strip()
    else:
        ingredient = ing_sstring.strip()

    # create the output dictionary
    output_dict = {'text': ing_string,
                   'ingredient': ingredient,
                   'quantity': quantity,
                   'measurement': measurement,
                   'descriptor': descriptor,
                   'preparation': preparation}

    quantity = '' if quantity is None else quantity
    quantity = str(quantity)
    quantities = quantity.split()
    fractions = utils.pmap(Fraction, quantities)
    quantity = sum(fractions)

    ret = Ingredient(quantity, measurement, ingredient, descriptor, preparation)
    return ret
