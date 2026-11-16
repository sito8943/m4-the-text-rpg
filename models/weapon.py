class Weapon:
    def __init__(self, name = "Unarmed", damage = 1):
        self.name = name
        self.damage = damage

    def __str__(self):
        return f"Weapon: {self.name}, Damage: {self.damage}"

    def to_dict(self):
        return {
            'name': self.name,
            'damage': self.damage
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['damage'])