"""Random exploration events: battle, treasure or nothing."""

import random

import managers.screen_manager as sm
import managers.battle_manager as bm
import managers.api_manager as api
from prefabs.events import EVENT_TYPES, EVENTS, TREASURE_GOLD
from prefabs.enemies import ENEMIES, create_enemy, create_api_enemy

class EventManager:
    """Picks and runs exploration events."""

    def __init__(self):
        """Creates the screen, battle and API managers used by the events."""
        self._screen_manager = sm.ScreenManager()
        self._battle_manager = bm.BattleManager()
        self._api_manager = api.ApiManager()

    def generate_event(self):
        """Returns a random event type from EVENT_TYPES."""
        return random.choice(EVENT_TYPES)

    def trigger_event(self, event_type, character):
        """Runs the event of the given type for the character."""
        if event_type == "battle":
            self._trigger_battle_event(character)
        elif event_type == "treasure":
            self._trigger_treasure_event(character)
        elif event_type == "nothing":
            self._trigger_nothing_event()
        else:
            self._screen_manager.message(f"Unknown event type: {event_type}", style="red")

    def _trigger_battle_event(self, character):
        """Spawns an enemy at the character's level and starts a battle."""
        event = EVENTS["battle"]
        enemy = self._spawn_enemy(character.level)
        story = event["story"] + (f"A wild {enemy.name} appears! Prepare for battle!",)
        self._screen_manager.print_event_screen(event["title"], story, event["style"])
        self._battle_manager.start(character, enemy)

    def _trigger_treasure_event(self, character):
        """Adds a random amount of gold to the character's wallet."""
        event = EVENTS["treasure"]
        gold = random.randint(*TREASURE_GOLD)
        character.wallet.gold += gold
        story = event["story"] + (f"You found {gold} gold! Total: {character.wallet.gold}",)
        self._screen_manager.print_event_screen(event["title"], story, event["style"])

    def _trigger_nothing_event(self):
        """Shows the 'nothing happens' story."""
        event = EVENTS["nothing"]
        self._screen_manager.print_event_screen(event["title"], event["story"], event["style"])

    def _spawn_enemy(self, level):
        """Returns a D&D API monster for the level, or a random prefab enemy if the API fails."""
        monster = self._api_manager.fetch_monster(level)
        if monster:
            return create_api_enemy(monster, level=level)
        return create_enemy(random.choice(list(ENEMIES)), level=level)
