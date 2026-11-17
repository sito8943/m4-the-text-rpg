import utils.stats as st

from models.character_class import CharacterClass
from models.weapon import Weapon
from models.inventory import Inventory
from models.wallet import Wallet

class Character:
    def __init__(self, name, cclass, weapon, inventory, level=1, hp=None, mp=None, xp=0, gold=0, defeated_enemies=None):
        self.name = name
        self.cclass = cclass
        self.weapon = weapon
        self.inventory = inventory
        self.wallet = Wallet(name, gold)
        self.level = level
        self.hp = st.max_hp(cclass, level) if hp is None else hp
        self.mp = st.max_mp(cclass, level) if mp is None else mp
        self.xp = xp
        self.defeated_enemies = set(defeated_enemies or [])

    def __str__(self):
        return (f"Character: {self.name} (level {self.level})\n"
                f"{self.cclass}\n"
                f"HP: {self.hp}/{st.max_hp(self.cclass, self.level)}\n"
                f"MP: {self.mp}/{st.max_mp(self.cclass, self.level)}\n"
                f"ATK: {st.attack_power(self.cclass, self.level)}\n"
                f"DEF: {st.defense_power(self.cclass, self.level)}\n"
                f"XP: {self.xp}/{st.xp_to_next_level(self.level)}\n"
                f"Gold: {self.wallet.gold}\n"
                f"Defeated: {', '.join(sorted(self.defeated_enemies)) or 'None'}\n"
                f"{self.weapon}")

    def attack(self, target):
        damage = st.attack_power(self.cclass, self.level) + self.weapon.damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)
        return damage

    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)
        print(f"{self.name} takes {damage} damage! Current health: {self.hp}")
        if self.hp == 0:
            print(f"{self.name} has been defeated!")

    def heal(self, amount):
        self.hp = min(self.hp + amount, st.max_hp(self.cclass, self.level))
        print(f"{self.name} heals for {amount}. Current health: {self.hp}")

    def restore_mp(self, amount):
        self.mp = min(self.mp + amount, st.max_mp(self.cclass, self.level))
        print(f"{self.name} restores {amount} MP. Current MP: {self.mp}")

    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} gains {amount} XP.")
        while self.xp >= st.xp_to_next_level(self.level):
            self.xp -= st.xp_to_next_level(self.level)
            self.level += 1
            self.hp = st.max_hp(self.cclass, self.level)
            self.mp = st.max_mp(self.cclass, self.level)
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
            "xp": self.xp,
            "gold": self.wallet.gold,
            "cclass": self.cclass.to_dict(),
            "weapon": self.weapon.to_dict(),
            "inventory": self.inventory.to_dict(),
            "defeated_enemies": sorted(self.defeated_enemies),
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
            xp=data.get("xp", 0),
            gold=data.get("gold", 0),
            defeated_enemies=data.get("defeated_enemies", []),
        )
