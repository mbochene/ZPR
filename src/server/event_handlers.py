from flask_socketio import SocketIO, send, emit
from session import Session

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
    if len(session.whoseSocket) == 2 and not session.isGameActive:
        for sid in session.whoseSocket:
            emit('startGame', room=sid)
        session.isGameActive = True

def handleDisconnection(socketId):
    if session.disconnectClient(socketId):
        emit('stopGame', broadcast=True)
    print('disconnected', session.getNumberOfConnectedClients())
    emit('disconnect', room=socketId)
