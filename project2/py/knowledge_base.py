import json
import utils
import random


class KnowledgeBase:
    def __init__(self, filepath):

        with open(filepath) as f:
            json_data = json.load(f)
            self.tools = json_data['tools']
            self.primary_methods = json_data['methods']['primary']
            self.secondary_methods = json_data['methods']['secondary']
            self.liquid_measurements = json_data['measurements']['liquids']
            self.solid_measurements = json_data['measurements']['solids']

            self.meat_descriptors = json_data['descriptors']['meat']
            self.veggie_descriptors = json_data['descriptors']['veggie']
            self.seafood_descriptors = json_data['descriptors']['seafood']
            self.seasoning_descriptors = json_data['descriptors']['seasoning']
            self.other_descriptors = json_data['descriptors']['other']
            self.style_descriptors = json_data['descriptors']['style']

            self.prep = json_data['preparation']['prep']
            self.hard_prep = json_data['preparation']['hard_prep']

            self.vegge_proteins = self._select_class(
                json_data['ingredients']['protein'], 'vegetarian')
            self.meats = utils.list_difference(
                json_data['ingredients']['protein'].keys(),
                self.vegge_proteins)

            self.scalable_ingredients = json_data['scalable']
            healthy_unhealthy_relations = json_data['healthy_unhealthy_subs']
            self.healthy_to_unhealthy = {
                healthy: unhealthy for healthy,
                unhealthy in healthy_unhealthy_relations}
            self.unhealthy_to_healthy = {
                unhealthy: healthy for healthy,
                unhealthy in healthy_unhealthy_relations}

            self.all_ingredients = json_data['ingredients']
            self.chinese_ingredients = {
                category: self._select_class(
                    dic,
                    'chinese') for category,
                dic in json_data['ingredients'].items()}

    def _select_class(self, dictionary, classification):
        """
            [dictionary] - dict of form {'item': ['class1', 'class2', ...]}
            [classification] - string
        """
        items = [
            item for item,
            classes in dictionary.items() if classification in classes]
        return items

    def _is_item_type(self, item, collection):
        for element in collection:
            if element in item:
                return True

        return False

    def _is_ingredient_type(self, ingredient, collection):
        return self._is_item_type(ingredient.name, collection)

    def is_meat(self, ingredient):
        ingredient_is_meat = self._is_ingredient_type(ingredient, self.meats)
        return ingredient_is_meat

    def is_vegge_protein(self, ingredient):
        ingredient_is_veg_protein = self._is_ingredient_type(
            ingredient, self.vegge_proteins)
        return ingredient_is_veg_protein

    def is_scalable_ingredient(self, ingredient):
        return self._is_ingredient_type(ingredient, self.scalable_ingredients)

    def is_unhealthy(self, ingredient):
        return self._is_ingredient_type(
            ingredient, self.unhealthy_to_healthy.keys())

    def is_healthy(self, ingredient):
        return self._is_ingredient_type(
            ingredient, self.healthy_to_unhealthy.keys())

    def _get_random_substitute(self, ingredient, collection):
        upper_bound = len(collection) - 1
        index = random.randint(0, upper_bound)
        chosen_sub = collection[index]
        return ingredient.substitute_name(chosen_sub)

    def _get_determinate_substitute(self, ingredient, collection):
        if ingredient.name in collection:
            sub = collection[ingredient.name]
            return ingredient.substitute_name(sub)

        else:
            return ingredient

    def get_healthy_substitute(self, ingredient):
        return self._get_determinate_substitute(
            ingredient, self.healthy_to_unhealthy)

    def get_unhealthy_substitute(self, ingredient):
        return self._get_determinate_substitute(
            ingredient, self.unhealthy_to_healthy)

    def get_meat_substitute(self, ingredient):
        protein = self._get_random_substitute(ingredient, self.vegge_proteins)
        return protein

    def get_meat(self, ingredient):
        meat = self._get_random_substitute(ingredient, self.meats)
        return meat

    def _find_category(self, ingredient, cuisine_context):
        """
            [ingredient] - Ingredient
            [context] - { 'protein':['chicken',...], ...}

            finds the category of food the ingredient belongs to in the context.
            return None if the ingredient is not found in the context
        """
        for category, ingredients in cuisine_context.items():
            if self._is_ingredient_type(ingredient, ingredients):
                return category

        return None

    def is_not_chinese_ingredient(self, ingredient):
        return self._find_category(
            ingredient, self.chinese_ingredients) is None

    def get_chinese_equivalent(self, ingredient):
        category = self._find_category(ingredient, self.all_ingredients)

        if not category:
            return ingredient.name

        sub = self._get_random_substitute(self.chinese_ingredients[category])

        return sub
