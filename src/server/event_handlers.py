from flask_socketio import SocketIO, send, emit
from engine import GameState

#game = GameState()

#whoNow = 'X'
#wonLocalBoards = []
# nieuzywane latelyPlayed = 9

class Game:
    def __init__(self):
        self.gameState = GameState()
        self.playableFields = [0,1,2,3,4,5,6,7,8,9]
        self.playerSymbol = ["none",'X','O']
    def makeMove(self, board, field):
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
    #global wonLocalBoards
    global game
    whoseTurn = game.playerSymbol[game.getWhoseTurn()]
    toLighten = []
    id = int(data['id'])
    board = id // 10
    field = id % 10
    correct = game.makeMove(board, field)
    #print(correct, board, field, wonLocalBoards)
    print(correct, board, field, game.playableFields)
    if(correct):
        inHtml = whoseTurn
        ######print(game.checkLocalWin())
        ######if(game.checkLocalWin() != 0):
        print(game.isBoardNotPlayable(board))
        if(game.isBoardNotPlayable(board)):
            game.playableFields.remove(board)

        nextBoard = game.getNextBoard()

        if(nextBoard == 9):
            toLighten = game.playableFields
        else:
            toLighten.append(nextBoard)
        
        data['inHtml'] = inHtml
        data['toLighten'] = toLighten
        print(toLighten)
        emit('respondToClickedField', data, broadcast=True)

def handleReceivedMessage(msg):
    print(msg)
    emit('respondToReceivedMessage', msg, broadcast=True)
