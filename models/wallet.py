"""Wallet model."""

class Wallet:
    """Gold owned by a character."""

    def __init__(self, owner_name, gold=0):
        """Creates a wallet for the owner with an amount of gold."""
        self.owner_name = owner_name
        self.gold = gold

    def add_gold(self, amount):
        """Adds gold to the wallet."""
        self.gold += amount
        print(f"{self.owner_name} gets {amount} gold. Total: {self.gold}")

    def spend_gold(self, amount):
        """Spends gold if there is enough. Returns True on success, False otherwise."""
        if amount > self.gold:
            print(f"Not enough gold. You have {self.gold}, need {amount}.")
            return False
        self.gold -= amount
        return True
