import random

import managers.screen_manager as sm
from prefabs.events import EVENT_TYPES, EVENTS, TREASURE_GOLD
from prefabs.enemies import ENEMIES, create_enemy

class EventManager:
    def __init__(self):
        self._screen_manager = sm.ScreenManager()

    def generate_event(self):
        return random.choice(EVENT_TYPES)

    def trigger_event(self, event_type, character):
        if event_type == "battle":
            self._trigger_battle_event(character)
        elif event_type == "treasure":
            self._trigger_treasure_event(character)
        elif event_type == "nothing":
            self._trigger_nothing_event()
        else:
            self._screen_manager.message(f"Unknown event type: {event_type}", style="red")

    def _trigger_battle_event(self, character):
        event = EVENTS["battle"]
        enemy = create_enemy(random.choice(list(ENEMIES)), level=character.level)
        story = event["story"] + (f"A wild {enemy.name} appears! Prepare for battle!",)
        self._screen_manager.print_event_screen(event["title"], story, event["style"])
        # Implement battle logic here

    def _trigger_treasure_event(self, character):
        event = EVENTS["treasure"]
        gold = random.randint(*TREASURE_GOLD)
        character.wallet.gold += gold
        story = event["story"] + (f"You found {gold} gold! Total: {character.wallet.gold}",)
        self._screen_manager.print_event_screen(event["title"], story, event["style"])

    def _trigger_nothing_event(self):
        event = EVENTS["nothing"]
        self._screen_manager.print_event_screen(event["title"], event["story"], event["style"])
