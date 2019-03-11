from fractions import Fraction


class Ingredient:
    def __init__(self, quantity, measure, name):
        self.quantity = Fraction(quantity) if quantity else Fraction(0)
        self.measure = measure if measure else ''
        self.name = name if name else ''

    def __str__(self):
        s = ' '.join([str(self.quantity), self.measure, self.name])
        return s

    def substitute_name(self, substitute_name):
        new_ingredient = Ingredient(
            self.quantity, self.measure, substitute_name)
        return new_ingredient

    def substitute_quantity(self, quantity):
        new_ingredient = Ingredient(
            quantity, self.measure, self.name)
        return new_ingredient

    def scale_quantity(self, factor):
        """
            scales quantity of ingredient by factor
        """
        new_quantity = self.quantity * Fraction(factor)
        new_ingredient = self.substitute_quantity(new_quantity)
        return new_ingredient
