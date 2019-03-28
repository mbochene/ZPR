from flask_socketio import SocketIO, send, emit
from engine import GameState
game = GameState()

whoNow = 'X'
wonLocalBoards = []
latelyPlayed = 9


def handleClickedField(data):
    global wonLocalBoards
    global game
    global whoNow
    toLighten = []
    id = int(data['id'])
    board = id // 10
    field = id % 10
    correct = game.makeMove(board, field)
    print(correct, board, field, wonLocalBoards)
    if(correct):
        inHtml = whoNow
        if(whoNow == 'X'):
            whoNow = 'O'
        else:
            whoNow = 'X'
        print(game.checkLocalWin())
        if(game.checkLocalWin() != 0):
            try:
                wonLocalBoards.index(board)
            except:
                wonLocalBoards.append(board)
        try:
            wonLocalBoards.index(field)
            for x in range(0, 9):
                try:
            	    wonLocalBoards.index(x)
                except:
                	toLighten.append(x)
        except:
            toLighten.append(field)
            pass
        data['inHtml'] = inHtml
        data['toLighten'] = toLighten
        print(toLighten)
        emit('respondToClickedField', data, broadcast=True)

def handleReceivedMessage(msg):
    print(msg)
    emit('respondToReceivedMessage', msg, broadcast=True)
