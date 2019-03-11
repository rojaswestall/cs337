import utils


class Recipe:
    def __init__(
            self,
            name='Name Placeholder',
            ingredients=[],
            directions=[],
            primary_method=[], 
            secondary_methods=[],
            tools=[]):
        self.name = name
        self.ingredients = ingredients
        self.directions = directions
        self.primary_method = primary_method
        self.secondary_methods = secondary_methods
        self.tools = tools

    def __str__(self):
        s = self._format_title(self.name)
        s += self._format_section('Ingredients', self.ingredients)
        s += self._format_section('Directions', self.directions)
        s += self._format_section('Primary Cooking Method', self.primary_method)
        s += self._format_section('Other Required Methods', self.secondary_methods)
        s += self._format_section('Tools', self.tools)
        return s

    def _format_section(self, title, lst):
        lst = utils.pmap(str, lst)
        lst = utils.pmap(lambda s: s.capitalize(), lst)
        s = '## ' + title + '\n\n- ' + '\n- '.join(lst) + '\n\n'
        return s

    def _format_title(self, name):
        s = '# ' + name + '\n\n'
        return s

    def modify_name(self, modifier):
        new_name = modifier + ' ' + self.name
        r = Recipe(
            name=new_name,
            ingredients=self.ingredients,
            directions=self.directions,
            primary_method=self.primary_method,
            secondary_methods=self.secondary_methods,
            tools=self.tools)
        return r
