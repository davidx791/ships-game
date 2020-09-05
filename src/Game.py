class Game:
    def __init__(self, player1, player2, currentPlayer = 1):
        self.player1 = player1 #1
        self.player2 = player2 #0
        self.currentPlayer = currentPlayer

    def goRound(self):
        if self.currentPlayer: #player 1 move
            winner = self.oneMove(self.player1,self.player2)
        else: #player 2 move
            winner = self.oneMove(self.player2,self.player1)
        self.currentPlayer = (self.currentPlayer + 1) % 2
        return winner

    def oneMove(self,player,opponent):
        shot, destroyedShip = self.chooseShot(player)
        self.deleteShotFromAvailableShots(player,shot)
        player.addShotOnShotBoard(shot,opponent.board)
        #edges
        if destroyedShip != None:
            for i in destroyedShip.edges:
                opponent.board.iloc[int(i[0]),int(i[1])] = 'X'
                player.board.iloc[int(i[0]),int(i[1])+12] = 'X'

        #for ship in opponent.ships:
         #   print('Ship: ',ship.start,'',ship.length,' ',ship.direction,' ',ship.edges)
        if not len(opponent.ships):
            return player

    def chooseShot(self,player):
        correctAnswer = False
        while not correctAnswer:
            if player.playerMode:
                player.showBoards()
                shot, destroyedShip = player.setInputField('Shot!: ')
            else:
                shot, destroyedShip = player.generateField(player.availableShotFields)
            correctAnswer = True if shot in player.availableShotFields else False
            #print('L: ',player.availableShotFields)
            if (not correctAnswer) and player.playerMode:
                print('This field was chosen before. Choose another!')
        else:
            return shot, destroyedShip


    def deleteShotFromAvailableShots(self,player,items):
        if type(items) != type(list):
            items = [items]
        for i in items:
            player.availableShotFields.remove(i)



