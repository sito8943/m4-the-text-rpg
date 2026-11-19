"""Turn-based battle between the player and an enemy."""

import random

import utils.stats as st
import managers.screen_manager as sm
import managers.log_manager as lm

FLEE_CHANCE = 0.5
VICTORY_HEAL = 0.3
BATTLE_OPTIONS = ("1. Attack", "2. Use potion", "3. Flee")

class BattleManager:
    """Runs a battle loop and writes every turn to the battle log."""

    def __init__(self):
        """Creates the screen and log managers used during the battle."""
        self._screen_manager = sm.ScreenManager()
        self._log_manager = lm.LogManager()

    def start(self, character, enemy):
        """Runs the battle loop until one side dies or the player flees."""
        self._log_manager.write_log(f"Battle started: {character.name} vs {enemy.name} (level {enemy.level})")

        actions = {
            "1": lambda: ([self._attack(character, enemy)], True),
            "2": lambda: self._use_potion(character),
            "3": lambda: self._flee(character, enemy),
        }

        while st.is_alive(character.hp) and st.is_alive(enemy.hp):
            choice = self._screen_manager.print_info_screen(
                "Battle", self._status(character, enemy), "red", prompt="Choose your action: ")
            if choice not in actions:
                self._screen_manager.message("Invalid choice.", style="red")
                continue
            result = actions[choice]()
            if result is None:
                return
            turn, enemy_turn = result
            if enemy_turn and st.is_alive(enemy.hp):
                turn.append(self._attack(enemy, character))
            self._screen_manager.print_event_screen("Battle", turn, "red")

        if st.is_alive(character.hp):
            self._victory(character, enemy)
        else:
            self._defeat(character, enemy)

    def _status(self, character, enemy):
        """Returns the lines with both HP bars and the battle options."""
        return [
            f"{character.name}  HP {character.hp}/{st.max_hp(character.cclass, character.level)}",
            f"{enemy.name}  HP {enemy.hp}/{st.max_hp(enemy.cclass, enemy.level)}",
            "",
        ] + list(BATTLE_OPTIONS)

    def _attack(self, attacker, target):
        """Makes the attacker hit the target, logs it and returns the turn text."""
        damage = attacker.attack(target)
        text = f"{attacker.name} hits {target.name} for {damage} damage."
        self._log_manager.write_log(text)
        return text

    def _use_potion(self, character):
        """Uses the first potion in the inventory. Returns (turn lines, enemy attacks?)."""
        potions = [item for item in character.inventory.items if item.item_type == "potion"]
        if not potions:
            return ["You have no potions!"], False
        potion = potions[0]
        potion.use(character)
        character.inventory.remove_item(potion)
        text = f"{character.name} used {potion.name}."
        self._log_manager.write_log(text)
        return [text], True

    def _flee(self, character, enemy):
        """Tries to escape. Returns None on success, or (turn lines, True) on failure."""
        if random.random() >= FLEE_CHANCE:
            self._log_manager.write_log(f"{character.name} failed to flee from {enemy.name}")
            return ["You failed to escape!"], True
        self._log_manager.write_log(f"{character.name} fled from {enemy.name}")
        self._screen_manager.print_event_screen("Battle", ("You run as fast as you can...", "You escaped!"), "yellow")
        return None

    def _victory(self, character, enemy):
        """Gives XP and gold, heals part of the HP, records the enemy and shows the victory screen."""
        old_level = character.level
        character.gain_xp(enemy.xp_reward)
        character.wallet.gold += enemy.gold_reward
        character.defeated_enemies.add(enemy.name)
        old_hp = character.hp
        character.heal(int(st.max_hp(character.cclass, character.level) * VICTORY_HEAL))
        story = (f"{enemy.name} has been defeated!",
                 f"You gain {enemy.xp_reward} XP and {enemy.gold_reward} gold.",
                 f"You catch your breath and recover {character.hp - old_hp} HP.")
        if character.level > old_level:
            story += (f"Level up! You are now level {character.level}!",)
        self._log_manager.write_log(f"{character.name} defeated {enemy.name} (+{enemy.xp_reward} XP, +{enemy.gold_reward} gold)")
        self._screen_manager.print_event_screen("Victory", story, "green")

    def _defeat(self, character, enemy):
        """Fully heals the character and shows the defeat screen."""
        character.hp = st.max_hp(character.cclass, character.level)
        self._log_manager.write_log(f"{character.name} was defeated by {enemy.name}")
        self._screen_manager.print_event_screen("Defeat", (
            f"{enemy.name} was too strong...",
            "You wake up at the edge of the void, fully healed.",
        ), "red")
