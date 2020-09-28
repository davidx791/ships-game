import src.Game as G
import src.Board as B

configured = False
while not configured:
    chosenMode = input('1 - Player vs Player\n2 - Player vs Computer\n3 - Computer vs Computer\nChoose game mode: ')
    if len(chosenMode) == 1:
        try:
            chosenModeInt = int(chosenMode)
        except:
            print('Incorrect choice! Try again.')
        else:
            configured = True
            if chosenModeInt == 1:
                player1Name = input('Choose name for Player 1: ')
                player2Name = input('Choose name for Player 2: ')
                b1 = B.Board(player1Name,1)
                b2 = B.Board(player2Name,1)
            elif chosenModeInt == 2:
                player1Name = input('Choose name for Player 1: ')
                b1 = B.Board(player1Name,1)
                b2 = B.Board('Computer')
            elif chosenModeInt == 3:
                b1 = B.Board('Computer 1')
                b2 = B.Board('Computer 2')
            else:
                configured = False
    else:
        print('Incorrect choice! Try again.')

g = G.Game(b1, b2)
print('\n'*5,'################################ GAME ##############################',sep='')
endGame = False
count = 0
while not endGame:
    print('\n\nRound: ',count)
    count += 1
    for i in range(2):
        winner = g.goRound()
        if winner != None:
            endGame = True
            break

count -= 1
print('Game over in ',count,' round. Winner is : ',winner.name,'!!')





