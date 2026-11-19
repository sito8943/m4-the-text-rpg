# How To

Guide to install, open and play THE TEXT-BASED RPG.

## How to run

**Requirements**
- Python 3.8 or newer.
- Internet is optional: enemies come from the D&D 5e API when there is a connection. Without it, the game uses saved or built-in enemies.

**Steps**
1. Open a terminal in the project folder.
2. Install the dependencies (only the first time):
   ```
   pip3 install -r requirements.txt
   ```
3. Start the game:
   ```
   python3 ./main.py
   ```

## How to play

**Controls:** type the number of an option and press Enter. Type `exit` in the home or game menu to close the game at any time.

**1. Start**
- **Start Game / Continue Game**: creates a new character, or continues the saved one.
- **New Game**: deletes the current character (it asks first) and creates a new one.

**2. Create your character**
- Type a name: at least 3 letters, only letters and spaces.
- Choose a class. Each one has different HP and attack, and its own starter weapon:

  | Class | Starter weapon |
  |---|---|
  | Warrior | Sword |
  | Hunter | Bow |
  | Rogue | Dagger |

- You start with 2 potions.

**3. Game menu**
| Option | What it does |
|---|---|
| Explore | Walk into the void. You may find a battle (most of the time), nothing, or a treasure with gold. |
| Character | Shows your class, HP, attack, defense, XP, gold, weapon and defeated enemies. |
| Inventory | Use a potion to recover HP. |
| Shop | Buy potions and better weapons with gold. |
| Log | Shows the last lines of the battle log. |
| Save | Saves your character in `game_data.json`. |
| Main Menu | Goes back to the home screen. |
| Exit | Closes the game. |

**4. Battles**
- **Attack**: hit the enemy. Then the enemy hits you.
- **Use potion**: recover HP with your first potion. Then the enemy hits you.
- **Flee**: 50% chance to escape. If you fail, the enemy hits you.
- **Win**: you get XP and gold, and recover a bit of HP. Enough XP makes you level up (more max HP and attack).
- **Lose**: you wake up fully healed, but without the rewards.

**Tips**
- Your HP is not refilled between battles or when you level up. Keep potions for hard fights.
- Save often: the game does not save when you exit.
