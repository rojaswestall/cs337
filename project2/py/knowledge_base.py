import json
import utils
import random
from recipe import Recipe


class KnowledgeBase:
    def __init__(self, filepath):

        with open(filepath) as f:
            json_data = json.load(f)
            self.meats = json_data['ingredients']['protein']['meats']
            self.vegge_proteins = json_data['ingredients']['protein']['vegetarian']

    def is_ingredient_type(self, ingredient, collection):
        is_type_bools = utils.pmap(lambda m: m in ingredient, collection)
        ingredient_is_type = any(is_type_bools)
        return ingredient_is_type

    def is_meat(self, ingredient):
        ingredient_is_meat = self.is_ingredient_type(ingredient, self.meats)
        return ingredient_is_meat

    def is_vegge_protein(self, ingredient):
        ingredient_is_veg_protein = self.is_ingredient_type(
            ingredient, self.vegge_proteins)
        return ingredient_is_veg_protein

    def get_substitute(self, collection):
        upper_bound = len(collection) - 1
        index = random.randint(0, upper_bound)
        chosen_sub = collection[index]
        return chosen_sub

    def get_meat_substitute(self):
        protein = self.get_substitute(self.vegge_proteins)
        return protein

    def get_meat(self):
        meat = self.get_substitute(self.meats)
        return meat
