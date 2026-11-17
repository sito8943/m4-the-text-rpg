import managers.screen_manager as sm
import managers.event_manager as em
import managers.log_manager as lm

class ActionManager:
    def __init__(self):
       self._screen_manager = sm.ScreenManager()
       self._event_manager = em.EventManager()
       self._log_manager = lm.LogManager()

    def _character(self, data):
        if data:
            self._screen_manager.print_character_screen(data)
        else:
            self._screen_manager.message("No character data available.", style="red")

    def _explore(self, data):
        event_type = self._event_manager.generate_event()
        self._event_manager.trigger_event(event_type, data)

    def _inventory(self):
        self._screen_manager.print_inventory_screen()
        # Implement inventory logic here

    def _shop(self):
        self._screen_manager.print_shop_screen()
        # Implement shop logic here

    def do_action(self, action, data=None):
        if action == "explore":
            self._explore(data=data)
        elif action == "inventory":
            self._inventory()
        elif action == "shop":
            self._shop()
        elif action == "log":
            self._log_manager.show_log()
        elif action == "character":
            self._character(data=data)  # Pass the actual character data here
        else:
            self._screen_manager.message(f"Unknown action: {action}", style="red")