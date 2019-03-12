import utils


class Recipe:
    def __init__(self, ingredients, directions, primary_method, secondary_methods, tools):
        self.ingredients = ingredients
        self.directions = directions
        self.primary_method = primary_method
        self.secondary_methods = secondary_methods
        self.tools = tools

    def __str__(self):
        ings = utils.pmap(str, self.ingredients)

        s = self._format_section('Ingredients', ings)
        s += self._format_section('Directions', self.directions)
        s += self._format_section('Primary Cooking Method', self.primary_method)
        s += self._format_section('Other Required Methods', self.secondary_methods)
        s += self._format_section('Tools', self.tools)
        return s

    def _format_section(self, title, lst):
        lst = utils.pmap(lambda s: s.capitalize(), lst)
        s = '## ' + title + '\n\n- ' + '\n- '.join(lst) + '\n\n'
        return s
