import src.Game as G
import src.Board as B

b1 = B.Board('Player 1')#, 1)
b2 = B.Board('Computer')
g = G.Game(b1, b2)
print('\n'*5,'################################ GAME ##############################',sep='')
endGame = False
count = 0
while not endGame:
    print('\n\nRound: ',count)
    winner = g.goRound()
    if winner != None:
        print('Game over. Winner is : ',winner.name,'!!')
        endGame = True
    count += 1
    if count == 200:
        endGame = True

