"""Routes game menu actions to the right screen or manager."""

import utils.stats as st
import managers.screen_manager as sm
import managers.event_manager as em
import managers.log_manager as lm

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
            self._screen_manager.print_character_screen(data)
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

    def _shop(self):
        """Shows the shop screen."""
        self._screen_manager.print_shop_screen()
        # Implement shop logic here

    def do_action(self, action, data=None):
        """Runs the action with the given name (explore, character, inventory, shop or log)."""
        if action == "explore":
            self._explore(data=data)
        elif action == "inventory":
            self._inventory(data)
        elif action == "shop":
            self._shop()
        elif action == "log":
            self._log_manager.show_log()
        elif action == "character":
            self._character(data=data)  # Pass the actual character data here
        else:
            self._screen_manager.message(f"Unknown action: {action}", style="red")