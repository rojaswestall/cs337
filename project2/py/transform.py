import utils
from recipe import Recipe
from fractions import Fraction


HEALTHY_TRANSFORMATION_FACTOR = 0.75
UNHEALTHY_TRANSFORMATION_FACTOR = 1.5


def to_vegetarian(recipe, kb):
    new_recipe = _base_transformer(
        recipe=recipe,
        predicate=kb.is_meat,
        substituter=kb.get_meat_substitute,
        new_name='Vegetarian')

    return new_recipe


def from_vegetarian(recipe, kb):
    new_recipe = _base_transformer(
        recipe=recipe,
        predicate=kb.is_vegge_protein,
        substituter=kb.get_meat,
        new_name='Meaty')

    return new_recipe


def to_healthy(recipe, kb):
    new_recipe = _change_quantities(
        recipe,
        kb.is_scalable_ingredient,
        HEALTHY_TRANSFORMATION_FACTOR)

    new_recipe = _base_transformer(
        recipe=new_recipe,
        predicate=kb.is_unhealthy,
        substituter=kb.get_unhealthy_substitute,
        new_name='Healthy')

    return new_recipe


def from_healthy(recipe, kb):
    new_recipe = _change_quantities(
        recipe,
        kb.is_scalable_ingredient,
        UNHEALTHY_TRANSFORMATION_FACTOR)

    new_recipe = _base_transformer(
        recipe=new_recipe,
        predicate=kb.is_healthy,
        substituter=kb.get_healthy_substitute,
        new_name='Unhealthy')

    return new_recipe


def _base_transformer(recipe, predicate, substituter, new_name):
    new_recipe = substitute_ingredients(
        recipe,
        predicate,
        substituter
    )

    new_recipe = new_recipe.modify_name(new_name)

    return new_recipe

def to_chinese(recipe, kb):
    substituter = _make_name_substituter(kb.get_chinese_equivalent)

    new_recipe = _substitute_ingredients(
        recipe, kb.is_not_chinese_ingredient, substituter)

    return new_recipe


def _scale_quantity(ingredient, factor):
    """
        scales quantity of ingredient by factor
    """
    new_quantity = ingredient.quantity * factor
    new_ingredient = ingredient.substitute_quantity(new_quantity)
    return new_ingredient


def _change_quantities(recipe, predicate, factor):
    """
        scale quantity of all ingredients in a recipe that satisfy predicate by factor
    """
    def ingredient_mapper(i):
        return i.scale_quantity(factor) if predicate(i) else i

    new_ingredients = utils.pmap(ingredient_mapper, recipe.ingredients)
    new_recipe = Recipe(
        name=recipe.name,
        ingredients=new_ingredients,
        directions=recipe.directions,
        methods=recipe.methods,
        tools=recipe.tools)

    return new_recipe


def substitute_ingredients(recipe, predicate, substituter):
    """
        substitute ingredients in recipe that satisfy predicate with ingredients generated by substituter
    """
    new_ingredients = []
    directions = list(recipe.directions)

    for ingredient in recipe.ingredients:

        if predicate(ingredient):

            substitute_ingredient = substituter(ingredient)

            new_ingredients.append(substitute_ingredient)

            directions = _fix_directions(
                ingredient.name, substitute_ingredient.name, directions)

        else:
            new_ingredients.append(ingredient)

    new_recipe = Recipe(
        name=recipe.name,
        ingredients=new_ingredients,
        directions=directions,
        primary_method=recipe.primary_method,
        secondary_methods=recipe.secondary_methods,
        tools=recipe.tools)

    return new_recipe


def _fix_directions(old_ingredient_name, new_ingredient_name, directions):
    """
        substitute old ingredient with new ingredient in all directions
    """
    new_directions = utils.pmap(
        lambda d: _fix_direction(
            old_ingredient_name,
            new_ingredient_name,
            d),
        directions)
    return new_directions


def _fix_direction(old_ingredient_name, new_ingredient_name, direction):
    """
        substitute old ingredient with new ingredient in direction
    """
    new_direction = direction.replace(old_ingredient_name, new_ingredient_name)

    tokens = old_ingredient_name.split()
    for token in tokens:
        new_direction = new_direction.replace(token, new_ingredient_name)

    return new_direction
