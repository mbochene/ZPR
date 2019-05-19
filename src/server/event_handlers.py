#!venv/bin/python3
import flask_socketio as fsio
import engine as en
import room
import string
import random

rooms = []


def generateRoomId(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def getRoomClientIsConnectedTo(socketId):
    for el in rooms:
        if el['room'].isClientConnected(socketId):
            return el['room']
    return None


def getRoomById(roomId):
    for el in rooms:
        if el['room'].id == roomId:
            return el['room']
    return None


def handleCreateRoom(data, socketId):
    roomId = str(socketId)[-2:] + generateRoomId(4) + str(socketId)[:2]
    newRoom = room.Room(
        socketId, roomId, data['roomName'], data['advancedMode'], float(data['playTime']))
    rooms.append({'socketId': socketId, 'room': newRoom})
    mode = 'casual'
    playTime = '-'
    if data['advancedMode']:
        mode = 'advanced'
        playTime = str(data['playTime']) + ' s'
    data = {
        'roomId': roomId,
        'roomName': data['roomName'],
        'mode': mode,
        'playTime': playTime
    }
    handleJoinRoom(data, socketId)
    fsio.emit('createRoom', data, broadcast=True)


def handleClickedField(data, socketId):
    room = getRoomClientIsConnectedTo(socketId)
    if room is None:
        return
    game = room.game
    if room.whoseSocket.get(socketId) is None or room.whoseSocket.get(socketId) != game.getWhoseTurn():
        return
    toLighten = []
    id = int(data['id'])
    board = id // 10
    field = id % 10
    correct = game.makeMove(board, field)
    if correct:
        if game.isBoardNotPlayable(board):
            game.playableFields.remove(board)

        nextBoard = game.getNextBoard()

        if nextBoard == 9:
            toLighten = game.playableFields
        else:
            toLighten.append(nextBoard)

        data['inHtml'] = game.whoseTurnSymbol
        data['toLighten'] = toLighten

        if game.checkLocalWin() == en.PlayerSymbol.none:
            data['localGameEnded'] = False
            data['localBoardWinner'] = ''
        else:
            data['localGameEnded'] = True
            data['localBoardWinner'] = game.whoseTurnSymbol

        globalWinner = game.checkGlobalWin()

        if globalWinner != en.PlayerSymbol.none:
            data['globalGameEnded'] = True
            data['globalGameWinner'] = data['localBoardWinner']
            game.scoreTable[game.whoseTurnSymbol] += 1
            game.prepareNewRound()
        else:
            data['globalGameEnded'] = False
        for sid in room.clients:
            fsio.emit('actualizeView', data, room=sid)


def handleReceivedMessage(data, socketId):
    room = getRoomClientIsConnectedTo(socketId)
    data['who'] = 'self'
    fsio.emit('receivedMessage', data, room=socketId)
    data['who'] = 'friend'
    for sid in room.clients:
        fsio.emit('receivedMessage', data, room=sid, include_self=False)


def handleJoinRoom(data, socketId):
    gameActivated = False
    room = getRoomById(data['roomId'])
    if room is not None:
        data['status'] = 'JOINED_ROOM'
        fsio.emit('joinRoom', data, room=socketId)
        room.connectClient(socketId)
        if len(room.whoseSocket) >= 2:
            if not room.isGameActive:
                gameActivated = True
                for sid in room.clients:
                    fsio.emit('startGame', room=sid)
                room.isGameActive = True
            else:
                fsio.emit('startGame', data, room=socketId)
    else:
        data['status'] = 'INVALID_ROOM_ID'
        fsio.emit('joinRoom', data, room=socketId)
    return gameActivated, room


def handleLeaveRoom(socketId):
    gameActivated = False
    room = getRoomClientIsConnectedTo(socketId)
    if room is not None:
        if room.disconnectClient(socketId):
            for sid in room.clients:
                fsio.emit('stopGame', room=sid)
            if room.numberOfConnectedClients >= 2:
                gameActivated = True
                room.isGameActive = True
                for sid in room.clients:
                    fsio.emit('startGame', room=sid)
    fsio.emit('stopGame', room=socketId)
    fsio.emit('leaveRoom', room=socketId)
    return gameActivated, room


def handleConnection(socketId):
    print(socketId + " connected")
    data = []
    for el in rooms:
        print(socketId + " connected")
        room = el['room']
        mode = 'casual'
        playTime = '-'
        if room.advancedMode:
            mode = str(room.playTime) + ' s'
        data.append(
            {'roomName': room.name,
             'mode': mode,
             'playTime': playTime,
             'roomId': room.id
             }
        )
    fsio.emit('initializeRoomsList', data, room=socketId)


def handleDisconnection(socketId):
    handleLeaveRoom(socketId)
    fsio.emit('disconnect', room=socketId)
