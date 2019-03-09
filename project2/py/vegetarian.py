import utils
from recipe import Recipe
from ingredient import Ingredient


def make_vegetarian(recipe, kb):
    new_recipe = substitute_ingredients(
        recipe, kb.is_meat, kb.get_meat_substitute)
    return new_recipe


def from_vegetarian(recipe, kb):
    new_recipe = substitute_ingredients(
        recipe, kb.is_vegge_protein, kb.get_meat)

    return new_recipe


def substitute_ingredients(recipe, identifier, substituter):
    new_ingredients = []
    directions = list(recipe.directions)

    for ingredient in recipe.ingredients:

        if identifier(ingredient.name):
            substitute_name = substituter()

            new_ingredient = ingredient.substitute(substitute_name)

            new_ingredients.append(new_ingredient)

            directions = fix_directions(
                ingredient.name, substitute_name, directions)

        else:
            new_ingredients.append(ingredient)

    new_recipe = Recipe(new_ingredients, directions)

    return new_recipe


def fix_directions(old_ingredient, new_ingredient, directions):
    new_directions = utils.pmap(
        lambda d: fix_direction(
            old_ingredient,
            new_ingredient,
            d),
        directions)
    return new_directions


def fix_direction(old_ingredient, new_ingredient, direction):
    new_direction = direction.replace(old_ingredient, new_ingredient)
    return new_direction
