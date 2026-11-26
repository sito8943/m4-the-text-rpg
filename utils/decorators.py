"""Custom decorators for the game."""

def requires_character(action):
    """Runs the action only if there is a character. Otherwise shows an error."""
    def wrapper(self, character):
        if not character:
            self._screen_manager.message("No character data available.", style="red")
            return
        return action(self, character)
    return wrapper
