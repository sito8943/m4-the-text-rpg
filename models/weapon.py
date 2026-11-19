"""Weapon model."""

class Weapon:
    """A weapon that adds damage to attacks."""

    def __init__(self, name = "Unarmed", damage = 1):
        """Creates a weapon. Defaults to 'Unarmed' with 1 damage."""
        self.name = name
        self.damage = damage

    def __str__(self):
        """Returns the weapon name and damage as text."""
        return f"Weapon: {self.name}, Damage: {self.damage}"

    def to_dict(self):
        """Returns the weapon as a dict that can be saved as JSON."""
        return {
            'name': self.name,
            'damage': self.damage
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a weapon from a dict made by to_dict."""
        return cls(data['name'], data['damage'])