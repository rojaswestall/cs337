import html2text
import urllib.request as url
from bs4 import BeautifulSoup
from recipe import Recipe
from parse_ingredients import parse_ingredients
import operator
import utils
from ingredient import Ingredient

INGREDIENTS_SELECTOR = '[itemprop="recipeIngredient"]'
DIRECTIONS_SELECTOR = '[itemprop="recipeInstructions"] span.recipe-directions__list--item'
NAME_SELECTOR = '#recipe-main-content'


def fetch_recipe(address, kb):
    response = url.urlopen(address)
    soup = BeautifulSoup(response, 'html.parser')

    ingredients = select_ingredients(soup)
    directions = select_directions(soup)

    primary_method = get_primary_method(directions, kb.primary_methods)
    secondary_methods = parse(directions, kb.secondary_methods)
    secondary_methods = [method for method in secondary_methods if method not in primary_method]
    tools = parse(directions, kb.tools)

    name = select_recipe_name(soup)
    ingredient_objs = parse_ingredients(ingredients, kb)
    tools = parse(directions, kb.tools)

    recipe_obj = Recipe(
        name=name,
        ingredients=ingredient_objs,
        directions=directions,
        primary_method=primary_method,
        secondary_methods=secondary_methods,
        tools=tools)

    return recipe_obj


def select_recipe_name(soup):
    name_node = soup.select_one(NAME_SELECTOR)
    return name_node.text.strip()


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
            lst.append(word)
    return lst

def get_primary_method(directions, seconday_methods):
    # Go through all directions & return whichever primary cooking method is mentioned most frequently.
    methods_dict = {}
    for direction in directions:
        direction = direction.lower().replace('.', '').split()
        for word in seconday_methods:
            if word in direction:
                if word in methods_dict:
                    methods_dict[word] += direction.count(word)
                else:
                    methods_dict[word] = 1

    if methods_dict == {}:
        return []
    sorted_methods = sorted(methods_dict.items(), key=operator.itemgetter(1))
    return [sorted_methods[0][0]]


if __name__ == '__main__':
    import sys

    address = sys.stdin.read()
    recipe = fetch_recipe(address)

    print(recipe)
