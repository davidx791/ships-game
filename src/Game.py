class Game:
    def __init__(self, player1, player2, mode = 1):
        self.player1 = player1
        self.player2 = player2
        self.mode = mode

    def nextTurn(self):
        self.mode = (self.mode + 1) % 2
