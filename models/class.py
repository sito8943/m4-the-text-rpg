class Class:
    def __init__(self, name, hp=100, mp=50, atk=10, defense=5, hp_multiplier=1.0, mp_multiplier=1.0, atk_multiplier=1.0, defense_multiplier=1.0):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.atk = atk
        self.defense = defense
        self.hp_multiplier = hp_multiplier
        self.mp_multiplier = mp_multiplier
        self.atk_multiplier = atk_multiplier
        self.defense_multiplier = defense_multiplier

    def level_up(self):
        self.hp += int(10 * self.hp_multiplier)
        self.mp += int(5 * self.mp_multiplier)
        self.atk += int(2 * self.atk_multiplier)
        self.defense += int(1 * self.defense_multiplier)