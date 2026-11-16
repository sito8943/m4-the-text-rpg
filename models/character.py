from models.character_class import CharacterClass
from models.weapon import Weapon
from models.inventory import Inventory


class Character:
    def __init__(self, name, cclass, weapon, inventory, level=1, hp=None, mp=None):
        self.name = name
        self.cclass = cclass
        self.weapon = weapon
        self.inventory = inventory
        self.level = level
        self.hp = self.max_hp() if hp is None else hp
        self.mp = self.max_mp() if mp is None else mp

    def max_hp(self):
        return self.cclass.hp + int(10 * self.cclass.hp_multiplier) * (self.level - 1)

    def max_mp(self):
        return self.cclass.mp + int(5 * self.cclass.mp_multiplier) * (self.level - 1)

    def attack_power(self):
        return self.cclass.atk + int(2 * self.cclass.atk_multiplier) * (self.level - 1)

    def defense_power(self):
        return self.cclass.defense + int(1 * self.cclass.defense_multiplier) * (self.level - 1)

    def __str__(self):
        return (f"Character: {self.name} (level {self.level})\n"
                f"{self.cclass}\n"
                f"HP: {self.hp}/{self.max_hp()}\n"
                f"MP: {self.mp}/{self.max_mp()}\n"
                f"ATK: {self.attack_power()}\n"
                f"DEF: {self.defense_power()}\n"
                f"{self.weapon}")

    def attack(self, target):
        damage = self.attack_power() + self.weapon.damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)
        return damage

    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)
        print(f"{self.name} takes {damage} damage! Current health: {self.hp}")
        if self.hp == 0:
            print(f"{self.name} has been defeated!")

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp())
        print(f"{self.name} heals for {amount}. Current health: {self.hp}")

    def level_up(self):
        self.level += 1
        self.hp = self.max_hp()
        self.mp = self.max_mp()
        print(f"{self.name} reached level {self.level}!")

    def equip_weapon(self, new_weapon):
        self.weapon = new_weapon
        print(f"{self.name} has equipped {new_weapon.name}.")

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "mp": self.mp,
            "cclass": self.cclass.to_dict(),
            "weapon": self.weapon.to_dict(),
            "inventory": self.inventory.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            cclass=CharacterClass.from_dict(data["cclass"]),
            weapon=Weapon.from_dict(data["weapon"]),
            inventory=Inventory.from_dict(data["inventory"]),
            level=data.get("level", 1),
            hp=data.get("hp"),
            mp=data.get("mp"),
        )
