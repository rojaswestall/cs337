
class Ingredient:
    def __init__(self, quantity, measure, name):
        self.quantity = quantity
        self.measure = measure
        self.name = name

    def __str__(self):
        s = ' '.join([self.quantity, self.measure, self.name])
        return s

    def substitute(self, substitute_name):
        new_ingredient = Ingredient(
            self.quantity, self.measure, substitute_name)
        return new_ingredient
