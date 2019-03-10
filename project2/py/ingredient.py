
class Ingredient:
    def __init__(self, quantity, measure, name):
        self.quantity = quantity if quantity else ''
        self.measure = measure if measure else ''
        self.name = name if name else ''

    def __str__(self):
        s = ' '.join([str(self.quantity), self.measure, self.name])
        return s

    def substitute(self, substitute_name):
        new_ingredient = Ingredient(
            self.quantity, self.measure, substitute_name)
        return new_ingredient
