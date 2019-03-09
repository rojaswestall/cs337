import utils
from recipe import Recipe
from ingredient import Ingredient


def make_vegetarian(recipe, kb):
    new_ingredients = []
    directions = list(recipe.directions)
    for ingredient in recipe.ingredients:

        if kb.is_meat(ingredient.name):
            meat_substitute = kb.get_meat_substitute()
            new_ingredient = ingredient.substitute(meat_substitute)
            new_ingredients.append(new_ingredient)
            directions = fix_directions(
                ingredient.name, meat_substitute, directions)

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
