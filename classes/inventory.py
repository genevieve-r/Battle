class Item:
    def __init__(self, name, type, description, prop, amount):
        self.name = name
        self.type = type
        self.description = description
        self.prop = prop
        self.amount = amount

    def get_item_amount(self):
        return self.amount

    def reduce_item_amount(self):
        self.amount -= 1

