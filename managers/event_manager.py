"""Random exploration events: battle, treasure or nothing."""

import random
import logging

import managers.ai_manager as ai
import managers.screen_manager as sm
import managers.battle_manager as bm
import managers.api_manager as api
from prefabs.events import EVENT_CHANCES, EVENTS, TREASURE_GOLD
from prefabs.enemies import ENEMIES, create_enemy, create_api_enemy

class EventManager:
    """Picks and runs exploration events."""

    def __init__(self):
        """Creates the screen, battle and API managers used by the events."""
        self._ai_manager = ai.AiManager()
        self._screen_manager = sm.ScreenManager()
        self._battle_manager = bm.BattleManager()
        self._api_manager = api.ApiManager()

    def generate_event(self):
        """Returns a random event type. Events with a bigger chance in EVENT_CHANCES come out more often."""
        roll = random.randint(1, 100)
        for event_type, chance in EVENT_CHANCES.items():
            if roll <= chance:
                return event_type
            roll -= chance
        return "nothing"

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
        intro = self._ai_manager.narrate(f"{character.name} meets a hostile {enemy.name}", event["story"])
        story = intro + (f"A wild {enemy.name} appears! Prepare for battle!",)
        self._screen_manager.print_event_screen(event["title"], story, event["style"])
        self._battle_manager.start(character, enemy)

    def _trigger_treasure_event(self, character):
        """Adds a random amount of gold to the character's wallet."""
        event = EVENTS["treasure"]
        gold = random.randint(*TREASURE_GOLD)
        character.wallet.gold += gold
        story = self._ai_manager.narrate(f"{character.name} finds a hidden treasure chest", event["story"])
        story = story + (f"You found {gold} gold! Total: {character.wallet.gold}",)
        self._screen_manager.print_event_screen(event["title"], story, event["style"])

    def _trigger_nothing_event(self):
        """Shows the 'nothing happens' story."""
        event = EVENTS["nothing"]
        story = self._ai_manager.narrate("the hero explores and nothing happens", event["story"])
        self._screen_manager.print_event_screen(event["title"], story, event["style"])

    def _spawn_enemy(self, level):
        """Returns a D&D API monster for the level, or a random prefab enemy if the API fails."""
        monster = self._api_manager.fetch_monster(level)
        if monster:
            return create_api_enemy(monster, level=level)
        logging.warning("API and cache failed, using prefab enemy")
        return create_enemy(random.choice(list(ENEMIES)), level=level)
