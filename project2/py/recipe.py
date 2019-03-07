import utils


class Recipe:
    def __init__(self, ingredients, directions):
        self.ingredients = ingredients
        self.directions = directions

    def __str__(self):
        ings = utils.pmap(str, self.ingredients)
        s = 'INGREDIENTS\n' + '\n'.join(ings) + '\n\n'
        s += 'DIRECTIONS\n' + '\n\n'.join(self.directions)
        return s
