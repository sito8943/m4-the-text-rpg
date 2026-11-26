"""Routes game menu actions to the right screen or manager."""

import utils.stats as st
import managers.screen_manager as sm
import managers.event_manager as em
import managers.log_manager as lm
from prefabs.items import ITEMS, create_item
from prefabs.weapons import WEAPONS, create_weapon
from prefabs.shop import SHOP_ITEMS, SHOP_WEAPONS

class ActionManager:
    """Runs the actions chosen in the game menu."""

    def __init__(self):
       """Creates the screen, event and log managers used by the actions."""
       self._screen_manager = sm.ScreenManager()
       self._event_manager = em.EventManager()
       self._log_manager = lm.LogManager()

    def _character(self, data):
        """Shows the character sheet, or an error if there is no character."""
        if data:
            wins = self._log_manager.count_wins(data.name)
            self._screen_manager.print_character_screen(data, wins)
        else:
            self._screen_manager.message("No character data available.", style="red")

    def _explore(self, data):
        """Generates a random event and triggers it for the character."""
        event_type = self._event_manager.generate_event()
        self._event_manager.trigger_event(event_type, data)

    def _inventory(self, character):
        """Shows the items in a loop. The player can use a potion or go back."""
        while True:
            items = character.inventory.items
            if not items:
                self._screen_manager.message("Your bag is empty.", title="Inventory")
                return

            # "1" -> first item, "2" -> second item... and the last number is Back
            options = {}
            labels = []
            for number, item in enumerate(items, start=1):
                options[str(number)] = item
                labels.append(f"{item.name}  ({item.description})")
            back = str(len(items) + 1)
            labels.append("Back")

            max_hp = st.max_hp(character.cclass, character.level)
            header = [f"HP {character.hp}/{max_hp}   Gold {character.wallet.gold}"]
            choice = self._screen_manager.print_menu("Inventory", labels, header)

            if choice == back:
                return
            if choice in options:
                self._use_item(character, options[choice])
            else:
                self._screen_manager.message("Invalid choice.", style="red")

    def _use_item(self, character, item):
        """Uses a potion and removes it from the inventory. Does nothing if the HP is already full."""
        if character.hp >= st.max_hp(character.cclass, character.level):
            self._screen_manager.message("Your HP is already full.", title="Inventory", style="yellow")
            return
        old_hp = character.hp
        item.use(character)
        character.inventory.remove_item(item)
        self._screen_manager.message(f"You used {item.name} and recovered {character.hp - old_hp} HP.",
                                     title="Inventory", style="green")

    def _shop(self, character):
        """Shows the shop in a loop. The player can buy potions and better weapons, or go back."""
        while True:
            # "1" -> (kind, key, price) of the first thing on sale... and the last number is Back
            options = {}
            labels = []
            for key, price in SHOP_ITEMS.items():
                item = ITEMS[key]
                options[str(len(options) + 1)] = ("item", key, price)
                labels.append(f"{item['name']:<11} {item['description']:<16} {price} g")
            for key, price in SHOP_WEAPONS.items():
                weapon = WEAPONS[key]
                if weapon["damage"] > character.weapon.damage:
                    options[str(len(options) + 1)] = ("weapon", key, price)
                    labels.append(f"{weapon['name']:<11} {'Damage ' + str(weapon['damage']):<16} {price} g")
            back = str(len(options) + 1)
            labels.append("Back")

            header = [f"Gold {character.wallet.gold}   Weapon: {character.weapon.name} ({character.weapon.damage})"]
            choice = self._screen_manager.print_menu("Shop", labels, header, style="yellow")

            if choice == back:
                return
            if choice in options:
                kind, key, price = options[choice]
                self._buy(character, kind, key, price)
            else:
                self._screen_manager.message("Invalid choice.", style="red")

    def _buy(self, character, kind, key, price):
        """Pays the price and gives the item (to the inventory) or the weapon (equipped). Fails without enough gold."""
        if not character.wallet.spend_gold(price):
            self._screen_manager.message(f"Not enough gold. You need {price} gold.", title="Shop", style="red")
            return
        if kind == "item":
            bought = create_item(key)
            character.inventory.add_item(bought)
        else:
            bought = create_weapon(key)
            character.equip_weapon(bought)
        self._screen_manager.message(f"You bought {bought.name} for {price} gold.", title="Shop", style="green")

    def do_action(self, action, data=None):
        """Runs the action with the given name (explore, character, inventory, shop or log)."""
        if action == "explore":
            self._explore(data=data)
        elif action == "inventory":
            self._inventory(data)
        elif action == "shop":
            self._shop(data)
        elif action == "log":
            self._log_manager.show_log()
        elif action == "character":
            self._character(data=data)  # Pass the actual character data here
        else:
            self._screen_manager.message(f"Unknown action: {action}", style="red")