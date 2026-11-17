import managers.screen_manager as sm

class ActionManager:
    def __init__(self):
       self._screen_manager = sm.ScreenManager()

    def _character(self, data):
        if data:
            self._screen_manager.show_screen("Character", str(data).split("\n"))
        else:
            self._screen_manager.show_screen("Character", ["No character data available."])
        self._screen_manager.pause("Press Enter to return to the game menu.")

    def _explore(self):
        self._screen_manager.show_screen("Explore", ["Exploring the world..."])
        # Implement exploration logic here
        self._screen_manager.pause("Press Enter to return to the game menu.")

    def _inventory(self):
        self._screen_manager.show_screen("Inventory", ["Inventory is currently empty."])
        # Implement inventory logic here
        self._screen_manager.pause("Press Enter to return to the game menu.")

    def _shop(self):
        self._screen_manager.show_screen("Shop", ["Welcome to the shop!"])
        # Implement shop logic here
        self._screen_manager.pause("Press Enter to return to the game menu.")

    def do_action(self, action, data=None):
        if action == "explore":
            self._explore()
        elif action == "inventory":
            self._inventory()
        elif action == "shop":
            self._shop()
        elif action == "character":
            self._character(data=data)  # Pass the actual character data here
        else:
            self._screen_manager.message(f"Unknown action: {action}")