"""Inventory model."""

from models.item import Item

class Inventory:
    """A list of items owned by a character."""

    def __init__(self):
        """Creates an empty inventory."""
        self.items = []

    def add_item(self, item):
        """Adds an item to the inventory."""
        self.items.append(item)
        print(f"Added {item} to inventory.")

    def remove_item(self, item):
        """Removes an item if it is in the inventory."""
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item} from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def list_items(self):
        """Prints all items in the inventory."""
        if self.items:
            print("Inventory items:")
            for item in self.items:
                print(f"- {item}")
        else:
            print("Inventory is empty.")

    def to_dict(self):
        """Returns the inventory as a dict that can be saved as JSON."""
        return {
            'items': [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an inventory from a dict made by to_dict."""
        inventory = cls()
        inventory.items = [Item.from_dict(item_data) for item_data in data.get('items', [])]
        return inventory