import html2text
import urllib.request as url
from bs4 import BeautifulSoup
from recipe import Recipe
from parse_ingredients import parse_ingredients

import utils
from ingredient import Ingredient

INGREDIENTS_SELECTOR = '[itemprop="recipeIngredient"]'
DIRECTIONS_SELECTOR = '[itemprop="recipeInstructions"] span.recipe-directions__list--item'


def fetch_recipe(address, kb):
    response = url.urlopen(address)
    soup = BeautifulSoup(response, 'html.parser')

    ingredients = select_ingredients(soup)
    ingredient_objs = parse_ingredients(ingredients)

    directions = select_directions(soup)
    methods = parse(directions, kb.methods)
    tools = parse(directions, kb.tools)

    recipe_obj = Recipe(ingredient_objs, directions, methods, tools)

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


def parse(directions, collection):
    matches = []
    for direction in directions:
        direction = direction.lower().replace('.,', '')
        matches.extend(extract(direction, collection))

    matches = list(set(matches))
    return matches


# takes a list from knowledge base and extracts any matches that are in
# the direction
def extract(direction, collection):
    lst = []
    for word in collection:
        if word in direction:
            lst.append(word.capitalize())
    return lst


if __name__ == '__main__':
    import sys

    address = sys.stdin.read()
    recipe = fetch_recipe(address)

    print(recipe)
