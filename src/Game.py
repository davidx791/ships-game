import src.Board as B

class Game:
    def __init__(self, player1, player2, currentPlayer = 1):
        self.player1 = player1 #1
        self.player2 = player2 #0
        self.currentPlayer = currentPlayer

    def nextTurn(self):
        if self.currentPlayer: #player 1
            shot = self.chooseShot(self.player1)
            self.deleteShotFromAvailableShots(self.player1,shot)
            self.player1.addShotOnShotBoard(shot,self.player2.board)
        else: #player 2
            shot = self.chooseShot(self.player2)
            self.deleteShotFromAvailableShots(self.player2,shot)
            self.player2.addShotOnShotBoard(shot,self.player1.board)

        self.currentPlayer = (self.currentPlayer + 1) % 2

    def chooseShot(self,player):
        correctAnswer = False
        while not correctAnswer:
            if player.playerMode:
                player.showBoards()
                shot = player.setInputField('Shot!: ')
            else:
                shot = player.generateField(player.availableShotFields)
            correctAnswer = True if shot in player.availableShotFields else False
            print('L: ',player.availableShotFields)
            if (not correctAnswer) and player.playerMode:
                print('This field was chosen before. Choose another!')
        else:
            return shot


    def deleteShotFromAvailableShots(self,player,items):
        if type(items) != type(list):
            items = [items]
        for i in items:
            player.availableShotFields.remove(i)



