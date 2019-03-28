from flask_socketio import SocketIO, send, emit
from engine import GameState

class Game:
    def __init__(self):
        self.prepareNewRound()
        self.playerSymbol = ["none",'X','O']
        self.scoreTable = {
            'X' : 0,
            'O' : 0
        }

    def prepareNewRound(self):
        self.gameState = GameState()
        self.playableFields = [0,1,2,3,4,5,6,7,8]

    def makeMove(self, board, field):
        self.whoseTurnSymbol = game.playerSymbol[game.getWhoseTurn()]
        return self.gameState.makeMove(board,field)

    def checkLocalWin(self):
        return self.gameState.checkLocalWin()

    def checkGlobalWin(self):
        return self.gameState.checkGlobalWin()

    def getWhoseTurn(self):
        return self.gameState.getWhoseTurn()

    def isBoardNotPlayable(self, board):
        return self.gameState.isBoardNotPlayable(board)

    def getNextBoard(self):
        return self.gameState.getNextBoard()

game=Game()

def handleClickedField(data):
    global game
    toLighten = []
    id = int(data['id'])
    board = id // 10
    field = id % 10
    correct = game.makeMove(board, field)
    print(correct, board, field, game.playableFields)
    if correct:
        print(game.isBoardNotPlayable(board))
        if game.isBoardNotPlayable(board):
            game.playableFields.remove(board)

        nextBoard = game.getNextBoard()

        if nextBoard == 9:
            toLighten = game.playableFields
        else:
            toLighten.append(nextBoard)
        
        data['inHtml'] = game.whoseTurnSymbol
        data['toLighten'] = toLighten
        
        if not game.checkLocalWin():
            data['localGameEnded'] = False
            data['localBoardWinner'] = ''
        else:
            data['localGameEnded'] = True
            data['localBoardWinner'] = game.whoseTurnSymbol

        print(toLighten)
        emit('actualizeView', data, broadcast=True)

def handleReceivedMessage(msg):
    print(msg)
    emit('respondToReceivedMessage', msg, broadcast=True)
