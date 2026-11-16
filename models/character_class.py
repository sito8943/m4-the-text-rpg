class CharacterClass:
    def __init__(self, name="No Class", hp=100, mp=50, atk=10, defense=5,
                 hp_multiplier=1.0, mp_multiplier=1.0, atk_multiplier=1.0, defense_multiplier=1.0):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.atk = atk
        self.defense = defense
        self.hp_multiplier = hp_multiplier
        self.mp_multiplier = mp_multiplier
        self.atk_multiplier = atk_multiplier
        self.defense_multiplier = defense_multiplier

    def __str__(self):
        return f"Class: {self.name}"

    def to_dict(self):
        return {
            'name': self.name,
            'hp': self.hp,
            'mp': self.mp,
            'atk': self.atk,
            'defense': self.defense,
            'hp_multiplier': self.hp_multiplier,
            'mp_multiplier': self.mp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'defense_multiplier': self.defense_multiplier
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['name'],
            data['hp'],
            data['mp'],
            data['atk'],
            data['defense'],
            data['hp_multiplier'],
            data['mp_multiplier'],
            data['atk_multiplier'],
            data['defense_multiplier']
        )
