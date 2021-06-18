class Settings:

    def __init__(self, grid_height=15,
                 grid_width=10,
                 actions=7):
        self.GRID_HEIGHT = grid_height
        self.GRID_WIDTH = grid_width

        self.STATES = self.GRID_WIDTH * self.GRID_HEIGHT
        self.ACTIONS = actions
