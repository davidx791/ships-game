class Game:
    def __init__(self, player1, player2, currentPlayer = 1):
        self.player1 = player1 #1
        self.player2 = player2 #0
        self.currentPlayer = currentPlayer

    def goRound(self):
        if self.currentPlayer: #player 1 move
            gameOver = self.oneMove(self.player1,self.player2)
        else: #player 2 move
            gameOver = self.oneMove(self.player2,self.player1)
        self.currentPlayer = (self.currentPlayer + 1) % 2
        return gameOver

    def oneMove(self,player,opponent):
        move = self.chooseShot(player,opponent)
        self.deleteShotFromAvailableShots(player,move)
        player.addShotOnShotBoard(move,opponent.board)

        if not len(opponent.ships):
             return player
        return None

    def chooseShot(self,player,opponent):
        correctAnswer = False
        while not correctAnswer:
            if player.playerMode:
                player.showBoards()
                print('Shot!: ')
                shot = player.setInputField()
            else:
                shot = player.generateField(player)
                if type(shot) != str: #gdy zestrzelono statek
                    destroyedShip = shot
                    for i in destroyedShip.edges:
                        opponent.board.iloc[int(i[0]),int(i[1])] = 'X'
                        player.board.iloc[int(i[0]),int(i[1])+12] = 'X'
                    self.updateOpponentShips(opponent.ships, destroyedShip)
                    shot = player.generateField(player)

            correctAnswer = True if shot in player.availableShotFields else False
            if (not correctAnswer) and player.playerMode:
                print('This field was chosen before. Choose another!')
        else:
            return shot

    def updateOpponentShips(self, ships, destroyed):
        for s in ships:
            if s.start == destroyed.start:
                ships.remove(s)
                break

    def deleteShotFromAvailableShots(self,player,items):
        if type(items) != list:
            items = [items]
        for i in items:
            if i in player.availableShotFields:
                player.availableShotFields.remove(i)



