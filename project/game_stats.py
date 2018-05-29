class GameStats():
    def __init__(self, settings):
        self.settings = settings
        self.game_active = True
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
