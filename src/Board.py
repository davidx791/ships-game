import pandas as pd
import random as rnd
import src.Ship as S
def char2index(char):
    return ord(char)-65

def index2char(index):
    return chr(index+65)

def col2opp(strCol):
    return int(strCol)+12

def opp2col(intCol):
    return str(intCol-12)

class Board:
    def __init__(self, name, mode = 0):
        self.name = name
        self.playerMode = mode
        self.board = self.createEmptyBoards()
        self.ships = self.setShips()
        self.availableShotFields = [i+str(c) for i in self.board.index for c in self.board.columns[:10]]
        self.lastGoodShots = []

    def createEmptyBoards(self):
        x = list(range(10))
        y = list(map(chr,range(65,75)))

        emptyContent = []
        for i in x:
            tmp = []
            for j in y:
                tmp += '-'
            emptyContent.append(tmp)

        #Columns - ships: int | shoots: string
        boardShips  = pd.DataFrame(emptyContent, columns=x, index=y)
        gap = pd.DataFrame([' ']*10, columns=[' '], index=y)
        chars = pd.DataFrame(y, columns=[' '], index=y)
        boardShoots = pd.DataFrame(emptyContent, columns=[str(i) for i in x], index=y)

        return pd.concat([boardShips, gap, chars, boardShoots], axis=1)

    def setShips(self):
        allShips = []

        #Direction 0:vertical 1:horizontal
        lengths = list(range(1,5))
        shipLengths_tmp = [str(i)*j for i, j in zip(list(reversed(lengths)), lengths)]
        shipLengths = [int(i) for ship in shipLengths_tmp for i in ship]

        for sLen in shipLengths:
            if self.playerMode:
                self.showBoards()
                print('Setting '+str(sLen)+'-masted: ')
            direction = self.chooseDirection(sLen,self.playerMode)
            chosenField = self.chooseStartField(sLen,direction,self.getAvailableFieldsOnShipsBoard(),self.playerMode)
            edges = self.addEdges4Ship(char2index(chosenField[0]), int(chosenField[1]), sLen,
                                       direction, self.getAvailableFieldsOnShipsBoard())
            s = S.Ship(chosenField,sLen,direction,edges)
            self.board = self.addShipOnBoard(s)
            allShips.append(s)

        self.cleanUpShipBoard()
        self.showBoards()

        return allShips

    def addEdges4Ship(self,id,col,l,d,availFields):
        if d:
            ids = list(range(id-1,id+2))
            cols = list(range(col-1,col+l+1))
        else:
            ids = list(range(id-1,id+l+1))
            cols = list(range(col-1,col+2))
        potentFields = [str(i)+str(c) for i in ids for c in cols]
        availFields = [str(char2index(i[0]))+i[1] for i in availFields]#zmiana chara na index
        return [i for i in potentFields if i in availFields] #edges

    def getAvailableFieldsOnShipsBoard(self):
        board = self.board.iloc[:, :10]
        allFields = [i+str(c) for i in list(board.index) for c in list(board.columns)]
        return [f for f in allFields if board.iloc[char2index(f[0]), int(f[1])] == '-']

    def getAvailableFieldsOnShotsBoard(self):
        board = self.board.iloc[:,12:]
        allFields = [i+str(c) for i in list(board.index) for c in list(board.columns)]
        return [f for f in allFields if board.iloc[char2index(f[0]), int(f[1])] == '-']

    def showBoards(self):
        print(self.name+':\n','\t'*3,'YOUR BOARD','\t'*6,'   OPPONENT BOARD\n',self.board,sep='')

    def addShipOnBoard(self,ship):
        st, l, d, e = ship.start, ship.length, ship.direction, ship.edges
        id = char2index(st[0])
        col = int(st[1])
        #setting ship with edges on board
        for i in e:
            self.board.iloc[int(i[0]),int(i[1])] = 'X'
        if d:
            self.board.iloc[id,col:col+l] = 'O'
        else:
            self.board.iloc[id:id+l,col] = 'O'

        return self.board

    def chooseDirection(self, sLen , playerMode):
        if playerMode:
            d = '1' if sLen == 1 else input('Ship orientation (0-vertical | 1-horizontal): ')
            while d != str(0) and d != str(1):
                d = input('Incorrect orientation. Choose again (0-vertical | 1-horizontal): ')
            else:
                return int(d)
        else:
            return rnd.randint(0,1)

    def chooseStartField(self,sLen,direction,availFields,playerMode):
        correctAnswer = False
        while not correctAnswer:
            if playerMode:
                print('Start field: ')
                start = self.setInputField()
            else:
                start = self.generateStartField()
            if direction:
                shipFields = [start[0]+str((int(start[1])+i)) for i in range(sLen)]
            else:
                shipFields = [str(index2char(char2index(start[0])+i))+start[1] for i in range(sLen)]
            lenCorrFields = len([sField for sField in shipFields if sField in availFields])
            correctAnswer = True if len(shipFields) == lenCorrFields else False
            if (not correctAnswer) and playerMode:
                print('Incorrect setting. Choose again!')
        else:
            return start


    def setInputField(self):
        while True:
            text = str(input()).upper()
            ind = char2index(text[0])
            if len(text) == 2 and ind >= 0 and ind <= 9:
                try:
                    tmpCol = int(text[1])
                except:
                    print('Incorrect input')
                else:
                    return text
            else:
                print('Incorrect input length or field')

    def generateStartField(self):
        ind = rnd.choice(list(map(chr,range(65,75))))
        col = rnd.choice(range(10))
        return ind+str(col)

    def getStartField(self,fields,direction):
        start = fields[0]
        for i in fields[1:]:
            if direction == 1: #poziom
                if start[1] > i[1]:
                    start = i
            else: #pion
                if char2index(start[0]) > char2index(i[0]):
                    start = i
        return start

    def generateField(self,player):
        if not len(player.lastGoodShots): # jeśli nie pamieta dobrego strzalu
            return rnd.choice(player.availableShotFields) #zwraca losowe pole
        else: #jesli pamieta
            result = self.getNeighboursAndDestroyedShip(player.lastGoodShots,player.availableShotFields)
            if type(result) == list:
                return rnd.choice(result) #zwraca sasiadow poprzednich strzalow
            else:
                player.lastGoodShots = []
                return result #zwraca statek

    def getNeighboursAndDestroyedShip(self,fields,availFields):
        if len(fields) == 1:
            ind = char2index(fields[0][0])
            col = fields[0][1]
            up = index2char(ind-1)+fields[0][1]
            down = index2char(ind+1)+fields[0][1]
            left = fields[0][0]+str(int(col)-1)
            right = fields[0][0]+str(int(col)+1)
            neighbours = [up,down,left,right]
            start = fields[0]
            direction = 1
        else: #>= 2
            if fields[0][0] == fields[1][0]:  #poziom
                cols = [int(fields[i][1]) for i in range(len(fields))]
                left = fields[0][0]+str(min(cols)-1)
                right = fields[0][0]+str(max(cols)+1)
                neighbours = [left,right]
                start = fields[0][0]+str(min(cols))
                direction = 1
            else: #pion
                inds = [char2index(fields[i][0]) for i in range(len(fields))]
                up =  index2char(min(inds)-1)+fields[0][1]
                down = index2char(max(inds)+1)+fields[0][1]
                neighbours = [up,down]
                start = index2char(min(inds))+fields[0][1]
                direction = 0

        correctNeighbours = [i for i in neighbours if i in availFields]
        if len(correctNeighbours) == 0:
            start = self.getStartField(fields,direction)
            edges = self.addEdges4Ship(char2index(start[0]), int(start[1]), len(fields),
                                       direction, self.getAvailableFieldsOnShotsBoard())
            return S.Ship(start,len(fields),direction,edges)

        return correctNeighbours

    def cleanUpShipBoard(self):
        self.board.iloc[:,:10] = self.board.iloc[:, :10].replace({'X':'-'})

    def addShotOnShotBoard(self, shot, opponentBoard):
        ind = char2index(shot[0]) #ind
        col = int(shot[1]) #col ship board
        col2 = col2opp(shot[1]) #col shot board

        if opponentBoard.iloc[ind, col] == 'O':
            opponentBoard.iloc[ind, col] = '!'
            self.board.iloc[ind, col2] = '!'
            self.lastGoodShots.append(shot)
        else:
            opponentBoard.iloc[ind, col] = 'X'
            self.board.iloc[ind, col2] = 'X'
        self.showBoards()
        print('Shot: ',shot)
