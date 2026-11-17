import managers.screen_manager as sm

class ActionManager:
    def __init__(self):
       self._screen_manager = sm.ScreenManager()

    def _character(self, data):
        if data:
            self._screen_manager.print_character_screen(data)
        else:
            self._screen_manager.message("No character data available.")

    def _explore(self):
        self._screen_manager.print_explore_screen()
        # Implement exploration logic here

    def _inventory(self):
        self._screen_manager.print_inventory_screen()
        # Implement inventory logic here

    def _shop(self):
        self._screen_manager.print_shop_screen()
        # Implement shop logic here

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