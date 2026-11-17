import utils.stats as st

from models.character import Character
from models.inventory import Inventory

class Enemy(Character):
    def __init__(self, name, cclass, weapon, level=1, xp_reward=10, gold_reward=5):
        super().__init__(name, cclass, weapon, Inventory(), level)
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward

    def __str__(self):
        return f"{self.name} (level {self.level}) HP: {self.hp}/{st.max_hp(self.cclass, self.level)}"
