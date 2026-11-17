import random

import utils.stats as st
import managers.screen_manager as sm
import managers.log_manager as lm

FLEE_CHANCE = 0.5
BATTLE_OPTIONS = ("1. Attack", "2. Use potion", "3. Flee")

class BattleManager:
    def __init__(self):
        self._screen_manager = sm.ScreenManager()
        self._log_manager = lm.LogManager()

    def start(self, character, enemy):
        self._log_manager.write_log(f"Battle started: {character.name} vs {enemy.name} (level {enemy.level})")
        last_turn = []
        while st.is_alive(character.hp) and st.is_alive(enemy.hp):
            choice = self._screen_manager.print_info_screen(
                "Battle", self._status(character, enemy, last_turn), "red", prompt="Choose your action: ")
            if choice == "1":
                last_turn = [self._attack(character, enemy)]
            elif choice == "2":
                used, text = self._use_potion(character)
                last_turn = [text]
                if not used:
                    continue
            elif choice == "3":
                if self._flee(character, enemy):
                    return
                last_turn = ["You failed to escape!"]
            else:
                last_turn = ["Invalid choice."]
                continue
            if st.is_alive(enemy.hp):
                last_turn.append(self._attack(enemy, character))
        if st.is_alive(character.hp):
            self._victory(character, enemy)
        else:
            self._defeat(character, enemy)

    def _status(self, character, enemy, last_turn):
        lines = [
            f"{character.name}  HP {character.hp}/{st.max_hp(character.cclass, character.level)}",
            f"{enemy.name}  HP {enemy.hp}/{st.max_hp(enemy.cclass, enemy.level)}",
            "",
        ]
        if last_turn:
            lines += last_turn + [""]
        return lines + list(BATTLE_OPTIONS)

    def _attack(self, attacker, target):
        damage = attacker.attack(target)
        text = f"{attacker.name} hits {target.name} for {damage} damage."
        self._log_manager.write_log(text)
        return text

    def _use_potion(self, character):
        potions = [item for item in character.inventory.items if item.item_type == "potion"]
        if not potions:
            return False, "You have no potions!"
        potion = potions[0]
        potion.use(character)
        character.inventory.remove_item(potion)
        text = f"{character.name} used {potion.name}."
        self._log_manager.write_log(text)
        return True, text

    def _flee(self, character, enemy):
        if random.random() >= FLEE_CHANCE:
            self._log_manager.write_log(f"{character.name} failed to flee from {enemy.name}")
            return False
        self._log_manager.write_log(f"{character.name} fled from {enemy.name}")
        self._screen_manager.print_event_screen("Battle", ("You run as fast as you can...", "You escaped!"), "yellow")
        return True

    def _victory(self, character, enemy):
        old_level = character.level
        character.gain_xp(enemy.xp_reward)
        character.wallet.gold += enemy.gold_reward
        character.defeated_enemies.add(enemy.name)
        story = (f"{enemy.name} has been defeated!",
                 f"You gain {enemy.xp_reward} XP and {enemy.gold_reward} gold.")
        if character.level > old_level:
            story += (f"Level up! You are now level {character.level}!",)
        self._log_manager.write_log(f"{character.name} defeated {enemy.name} (+{enemy.xp_reward} XP, +{enemy.gold_reward} gold)")
        self._screen_manager.print_event_screen("Victory", story, "green")

    def _defeat(self, character, enemy):
        character.hp = st.max_hp(character.cclass, character.level)
        self._log_manager.write_log(f"{character.name} was defeated by {enemy.name}")
        self._screen_manager.print_event_screen("Defeat", (
            f"{enemy.name} was too strong...",
            "You wake up at the edge of the void, fully healed.",
        ), "red")
