import src.Game as G
import src.Board as B

b1 = B.Board('Player 1')#, 1)
b2 = B.Board('Computer')
g = G.Game(b1, b2)
print('\n'*5,'################################ GAME ##############################',sep='')
endGame = False
count = 0
while not endGame:
    print('Round: ',count)
    g.nextTurn()
    count += 1
    if count == 200:
        endGame = True

