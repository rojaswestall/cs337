import utils

class Recipe:
    def __init__(self, ingredients, directions, methods, tools):
        self.ingredients = ingredients
        self.directions = directions
        self.methods = methods
        self.tools = tools

    def __str__(self):
        ings = utils.pmap(str, self.ingredients)
        mthds = utils.pmap(str, self.methods)
        tls = utils.pmap(str, self.tools)

        s = 'INGREDIENTS\n' + '\n'.join(ings) + '\n\n'
        s += 'DIRECTIONS\n' + '\n\n'.join(self.directions) + '\n\n'
        s += 'METHODS\n' + '\n'.join(mthds) + '\n\n'
        s += 'TOOLS \n' + '\n'.join(tls)
        return s
