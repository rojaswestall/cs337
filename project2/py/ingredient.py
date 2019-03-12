from fractions import Fraction


class Ingredient:
    def __init__(self, quantity, measure, name, descriptor, preparation):
        self.quantity = Fraction(quantity) if quantity else Fraction(0)
        self.measure = measure if measure else ''
        self.name = name if name else ''
        self.descriptor = descriptor if descriptor else ''
        self.preparation = preparation if preparation else ''

    def __str__(self):
        s = [self.name,
        'Quantity: ' + str(self.quantity), 
        'Measurement: ' + self.measure if self.measure is not '' else '', 
        'Preparation: ' + self.preparation if self.preparation is not '' else '', 
        'Descriptor: ' + self.descriptor if self.descriptor is not '' else '']
        s = '\n  - '.join(filter(lambda x: x != '', s))
        return s

    def substitute_name(self, substitute_name):
        new_ingredient = Ingredient(
            self.quantity, self.measure, substitute_name, None, None)
        return new_ingredient

    def substitute_quantity(self, quantity):
        new_ingredient = Ingredient(
            quantity, self.measure, self.name, self.descriptor, self.preparation)
        return new_ingredient

    def scale_quantity(self, factor):
        """
            scales quantity of ingredient by factor
        """
        new_quantity = self.quantity * Fraction(factor)
        new_ingredient = self.substitute_quantity(new_quantity)
        return new_ingredient
