import utils


class Recipe:
    def __init__(self, ingredients, directions, methods, primary_method, tools):
        self.ingredients = ingredients
        self.directions = directions
        self.methods = methods
        self.primary_method = primary_method
        self.tools = tools

    def __str__(self):
        ings = utils.pmap(str, self.ingredients)

        s = self._format_section('Ingredients', ings)
        s += self._format_section('Directions', self.directions)
        s += 'Primary Method\n' + self.primary_method.capitalize() + '\n\n'
        s += self._format_section('Methods', self.methods)
        s += self._format_section('Tools', self.tools)
        return s
        
    def _format_section(self, title, lst):
        lst = utils.pmap(lambda s: s.capitalize(), lst)
        s = '## ' + title + '\n\n- ' + '\n- '.join(lst) + '\n\n'
        return s
