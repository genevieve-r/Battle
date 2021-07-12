import random

class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

        #self means a particular instance of the class, so you can use the class to create the different instance of the spell

    def generate_spell_damage(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)

