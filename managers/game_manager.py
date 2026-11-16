class GameManager:
    def __init__(self):
        self.status = "initialized"

    def start_game(self):
        self.status = "started"
        print("Game has started.")