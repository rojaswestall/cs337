import html2text
import urllib.request as url
from bs4 import BeautifulSoup


def fetch_recipe(address):
    response = url.urlopen(address)
    soup = BeautifulSoup(response, 'html.parser')

    ingredients = select_ingredients(soup)

    directions = select_directions(soup)

    recipe_info = {'ingredients': ingredients, 'directions': directions}

    return recipe_info


def select_ingredients(soup):
    ingredients_selector = '[itemprop="recipeIngredient"]'

    ingredients = soup.select(ingredients_selector)
    ingredients = nodes_to_text(ingredients)
    return ingredients


def select_directions(soup):
    directions_selector = '[itemprop="recipeInstructions"] span'
    directions = soup.select(directions_selector)
    directions = nodes_to_text(directions)
    return directions


def nodes_to_text(nodes):
    return [node.text for node in nodes]


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
