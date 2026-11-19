"""Item model."""

class Item:
    """An item with a type and an effect (e.g. {'hp': 30})."""

    def __init__(self, name, description, item_type, effect):
        """Creates an item."""
        self.name = name
        self.description = description
        self.item_type = item_type
        self.effect = effect

    def use(self, target):
        """Applies the item effect to the target. Only potions can be used."""
        if self.item_type == "potion":
            print(f"{target.name} used {self.name}.")
            for stat, value in self.effect.items():
                if stat == "hp":
                    target.heal(value)
                elif stat == "mp":
                    target.restore_mp(value)
                else:
                    print(f"Unknown effect: {stat}.")
        else:
            print(f"{self.name} cannot be used directly.")

    def __str__(self):
        """Returns the item name, type and effect as text."""
        return f"Item: {self.name}, Type: {self.item_type}, Effect: {self.effect}"

    def to_dict(self):
        """Returns the item as a dict that can be saved as JSON."""
        return {
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type,
            'effect': self.effect
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an item from a dict made by to_dict."""
        return cls(data['name'], data['description'], data['item_type'], data['effect'])