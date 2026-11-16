class Item:
    def __init__(self, name, description, item_type, effect):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.effect = effect

    def use(self, target):
        if self.item_type == "potion":
            for stat, value in self.effect.items():
                if hasattr(target, stat):
                    setattr(target, stat, getattr(target, stat) + value)
                    print(f"{target.name} used {self.name} and gained {value} {stat}.")
                else:
                    print(f"{target.name} does not have {stat}.")
        else:
            print(f"{self.name} cannot be used directly.")

    def __str__(self):
        return f"Item: {self.name}, Type: {self.item_type}, Effect: {self.effect}"

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type,
            'effect': self.effect
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['description'], data['item_type'], data['effect'])