from nltk import pos_tag
from nltk import RegexpParser
import utils


def parse_ingredients(ingredients):
    return [parse_ingredient(ingredient) for ingredient in ingredients]


def parse_ingredient(ingredient):
    ingredient = ingredient.split()
    tokens_tag = pos_tag(ingredient)
    patterns = r"""
    quantity:{<CD>{1}}
    measure:{<NN>{1}}
    """
    chunker = RegexpParser(patterns)
    output = chunker.parse(tokens_tag)

    return output

def get_quantity(tags):
    pass

if __name__ == '__main__':
    import sys

    ingredients = sys.stdin.readlines()
    # print('INGREDIENTS', ingredients)
    parsed_ingredients = parse_ingredients(ingredients)

    # print('PARSED INGREDIENTS')
    utils.print_list(parsed_ingredients)
