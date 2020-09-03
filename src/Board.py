import pandas as pd
import src.Ship as S
def char2index(char):
    return ord(char)-65
def index2char(index):
    return chr(index+65)

class Board:
    def __init__(self, name):
        self.name = name
        self.board = self.createEmptyBoards()
        self.ships = self.setShips()


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
            self.showBoards()
            print('Setting '+str(sLen)+'-masted: ')
            direction = self.chooseDirection(sLen)
            chosenField = self.chooseStartField(sLen,direction,self.getAvailableFieldsOnShipsBoard())
            edges = self.addEdges4Ship( char2index(chosenField[0]), int(chosenField[1]), sLen,
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
        edges = [i for i in potentFields if i in availFields]
        return edges

    def getAvailableFieldsOnShipsBoard(self):
        board = self.board.iloc[:, :10]
        allFields = [i+str(c) for i in list(board.index) for c in list(board.columns)]
        return [f for f in allFields if board.iloc[char2index(f[0]), int(f[1])] == '-']

    def showBoards(self):
        print('\n\n',self.name+' move:\n','\t'*3,'YOUR BOARD','\t'*6,'   OPPONENT BOARD\n',self.board,sep='')

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

    def chooseDirection(self,sLen):
        d = '1' if sLen == 1 else input('Ship orientation (0-vertical | 1-horizontal): ')
        while d != str(0) and d != str(1):
            d = input('Incorrect orientation. Choose again (0-vertical | 1-horizontal): ')
        else:
            return int(d)

    def chooseStartField(self,sLen,direction,availFields):
        correctAnswer = False
        while not correctAnswer:
            start = str(input('Start field: '))[:2].upper()
            try:
                tmp = int(start[1])
            except:
                print('Incorrect input')
            else:
                if direction:
                    shipFields = [start[0]+str((int(start[1])+i)) for i in range(sLen)]
                else:
                    shipFields = [str(index2char(char2index(start[0])+i))+start[1] for i in range(sLen)]
                lenCorrFields = len([sField for sField in shipFields if sField in availFields])
                correctAnswer = True if len(shipFields) == lenCorrFields else False
                if not correctAnswer:
                    print('Incorrect setting. Choose again!')
        else:
            return start

    def cleanUpShipBoard(self):
        self.board = self.board.iloc[:, :10].replace({'X':'-'})


