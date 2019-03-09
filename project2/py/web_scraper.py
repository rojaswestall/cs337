import html2text
import urllib.request as url
from bs4 import BeautifulSoup
from recipe import Recipe

import utils
from ingredient import Ingredient

INGREDIENTS_SELECTOR = '[itemprop="recipeIngredient"]'
DIRECTIONS_SELECTOR = '[itemprop="recipeInstructions"] span'

def fetch_recipe(address, kb):
    response = url.urlopen(address)
    soup = BeautifulSoup(response, 'html.parser')

    ingredients = select_ingredients(soup)
    ingredient_objs = parse_ingredients(ingredients)

    directions = select_directions(soup)
    methods = parse_methods(directions, kb)
    tools = parse_tools(directions, kb)

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


def parse_ingredients(ingredients):
    objs = utils.pmap(Ingredient, ingredients)
    return objs

def parse_methods(directions, kb):
    allMethods = []
    for direction in directions:
        direction = direction.lower().replace('.,', '')
        allMethods.extend(extract_methods(direction, kb))

    allMethods = list(set(allMethods))
    return allMethods

def parse_tools(directions, kb):
    allTools = []
    for direction in directions:
        direction = direction.lower().replace('.,', '')
        allTools.extend(extract_tools(direction, kb))

    allTools = list(set(allTools))
    return allTools

def extract_methods(direction, kb):
    methods = []
    for word in kb.methods:
        if word in direction:
            methods.append(word.capitalize())
    return methods

def extract_tools(direction, kb):
    tools = []
    for word in kb.tools:
        if word in direction:
            tools.append(word.capitalize())
    return tools

def remove_dupes(str):
    newList = []
    [newList.append(word) for word in str if word not in newList]
    return newList

if __name__ == '__main__':
    import sys

    address = sys.stdin.read()
    recipe = fetch_recipe(address, kb)

    print('ADDRESS')
    print(address, '\n')

    print('INGREDIENTS')
    for i in recipe['ingredients']:
        print(i)

    print('\nDIRECTIONS')
    for i, step in enumerate(recipe['directions']):
        print('STEP' + str(i + 1) + '\n', step)
