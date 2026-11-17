class Wallet:
    def __init__(self, owner_name, gold=0):
        self.owner_name = owner_name
        self.gold = gold

    def add_gold(self, amount):
        self.gold += amount
        print(f"{self.owner_name} gets {amount} gold. Total: {self.gold}")

    def spend_gold(self, amount):
        if amount > self.gold:
            print(f"Not enough gold. You have {self.gold}, need {amount}.")
            return False
        self.gold -= amount
        return True
