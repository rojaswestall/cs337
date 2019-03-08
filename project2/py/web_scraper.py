import html2text
import urllib.request as url
from bs4 import BeautifulSoup
from recipe import Recipe

import utils
from ingredient import Ingredient

INGREDIENTS_SELECTOR = '[itemprop="recipeIngredient"]'
DIRECTIONS_SELECTOR = '[itemprop="recipeInstructions"] span'


def fetch_recipe(address):
    response = url.urlopen(address)
    soup = BeautifulSoup(response, 'html.parser')

    ingredients = select_ingredients(soup)
    ingredient_objs = parse_ingredients(ingredients)

    directions = select_directions(soup)

    recipe_obj = Recipe(ingredient_objs, directions)

    return recipe_obj


def select_ingredients(soup):

    ingredients = soup.select(INGREDIENTS_SELECTOR)
    ingredients = nodes_to_text(ingredients)
    return ingredients


def select_directions(soup):
    directions = soup.select(DIRECTIONS_SELECTOR)
    directions = nodes_to_text(directions)
    return directions


def nodes_to_text(nodes):
    return [node.text for node in nodes]


def parse_ingredients(ingredients):
    objs = utils.pmap(Ingredient, ingredients)
    return objs


if __name__ == '__main__':
    import sys

    address = sys.stdin.read()
    recipe = fetch_recipe(address)

    print('ADDRESS')
    print(address, '\n')

    print('INGREDIENTS')
    for i in recipe['ingredients']:
        print(i)

    print('\nDIRECTIONS')
    for i, step in enumerate(recipe['directions']):
        print('STEP' + str(i + 1) + '\n', step)
