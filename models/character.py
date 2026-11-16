class Character:
    def __init__(self, name, cclass, weapon):
        self.name = name
        self.cclass = cclass
        self.weapon = weapon

    def __str__(self):
        return f"Character: {self.name}, Health: {self.cclass.current_hp}, Weapon: {self.weapon}"

    def attack(self, target):
        damage = self.cclass.current_atk + self.weapon.damage
        target.cclass.current_hp -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        return damage

    def is_alive(self):
        return self.cclass.current_hp > 0

    def level_up(self):
        self.cclass.level_up()
        print(f"{self.name} has leveled up! New stats: Health: {self.cclass.current_hp}, Attack: {self.cclass.current_atk}, Defense: {self.cclass.current_defense}")

    def heal(self, amount):
        self.cclass.current_hp = min(self.cclass.current_hp + amount, self.cclass.hp)
        print(f"{self.name} heals for {amount}. Current health: {self.cclass.current_hp}")

    def equip_weapon(self, new_weapon):
        self.weapon = new_weapon
        print(f"{self.name} has equipped {new_weapon.name}.")

    def take_damage(self, damage):
        self.cclass.current_hp -= damage
        print(f"{self.name} takes {damage} damage! Current health: {self.cclass.current_hp}")
        if self.cclass.current_hp <= 0:
            print(f"{self.name} has been defeated!")