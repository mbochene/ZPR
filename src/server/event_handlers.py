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
    
    def prepareNewGame(self):
        self.prepareNewRound()
        self.scoreTable['X'] = 0
        self.scoreTable['O'] = 0

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

class Session:
    def __init__(self):
        self.numberOfConnectedClients = 0
        self.clients = []
        self.whoseSocket = {}
        self.game = Game()

    def connectClient(self, socketId):
        self.numberOfConnectedClients += 1
        if self.numberOfConnectedClients <= 2:
            self.whoseSocket[socketId] = self.numberOfConnectedClients

    def disconnectClient(self, socketId):
        self.numberOfConnectedClients -= 1
        if self.whoseSocket.get(socketId) != None:
            self.game.prepareNewGame()
            self.whoseSocket.pop(socketId)
            for socket in self.whoseSocket:             # jak 1 gracz sie odlaczy, to 2 gracz ma stac sie 1 graczem
                self.whoseSocket[socket] = 1            # dodac emita restartujacego gre
            emit('stopGame', broadcast=True)
            
    def getNumberOfConnectedClients(self):
        return self.numberOfConnectedClients
    
session = Session()
game = session.game

def handleClickedField(data, socketId):
    global game
    global session
    print(session.whoseSocket.get(socketId))
    if session.whoseSocket.get(socketId) != game.getWhoseTurn():
        return
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
        
        globalWinner = game.checkGlobalWin()

        if globalWinner != 0:
            data['globalGameEnded'] = True
            game.scoreTable[game.whoseTurnSymbol] += 1
            game.prepareNewRound()
        else:
            data['globalGameEnded'] = False

        print(toLighten)
        emit('actualizeView', data, broadcast=True)

def handleReceivedMessage(msg):
    print(msg)
    emit('respondToReceivedMessage', msg, broadcast=True)

def handleConnection(socketId):
    session.connectClient(socketId)
    print('connected', session.getNumberOfConnectedClients())
    if(session.getNumberOfConnectedClients() == 2):
        emit('startGame', broadcast=True)

def handleDisconnection(socketId):
    session.disconnectClient(socketId)
    print('disconnected', session.getNumberOfConnectedClients())
