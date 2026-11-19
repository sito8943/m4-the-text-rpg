"""Stat formulas that depend on class and level."""

# --- Stats Utilities ---

def xp_to_next_level(level):
    """Returns the XP needed to reach the next level."""
    return 50 * level

def max_hp(cclass, level):
    """Returns the max HP for a class at the given level."""
    return cclass.hp + int(10 * cclass.hp_multiplier) * (level - 1)

def max_mp(cclass, level):
    """Returns the max MP for a class at the given level."""
    return cclass.mp + int(5 * cclass.mp_multiplier) * (level - 1)

def attack_power(cclass, level):
    """Returns the attack power for a class at the given level."""
    return cclass.atk + int(2 * cclass.atk_multiplier) * (level - 1)

def defense_power(cclass, level):
    """Returns the defense power for a class at the given level."""
    return cclass.defense + int(1 * cclass.defense_multiplier) * (level - 1)

def is_alive(hp):
    """Returns True if the HP is above zero."""
    return hp > 0
