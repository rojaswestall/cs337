import json
import utils
import random
from recipe import Recipe


class KnowledgeBase:
    def __init__(self, filepath):

        with open(filepath) as f:
            json_data = json.load(f)
            self.meats = json_data['meats']
            self.meat_substitutes = json_data['meat-substitutes']

    def is_meat(self, food):
        is_meat_bools = utils.pmap(lambda m: m in food, self.meats)
        food_is_meat = any(is_meat_bools)
        return food_is_meat

    def get_meat_substitute(self):
        upper_bound = len(self.meat_substitutes) - 1
        index = random.randint(0, upper_bound)
        chosen_sub = self.meat_substitutes[index]
        return chosen_sub
