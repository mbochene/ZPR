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
        socketId, roomId, data['roomName'], data['advancedMode'], int(data['playTime']))
    rooms.append({'socketId': socketId, 'room': newRoom})
    mode = 'casual'
    playTime = '-'
    if data['advancedMode']:
        mode = 'advanced'
        playTime = str(data['playTime']) + ' s'
    createData = {
        'roomId': roomId,
        'roomName': data['roomName'],
        'mode': mode,
        'playTime': playTime
    }
    joinData = {
        'roomId': roomId
    }
    handleJoinRoom(joinData, socketId)
    fsio.emit('createRoom', createData, broadcast=True)


def handleClickedField(data, socketId):
    viewData = {
        'id': data['id']
    }
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

        viewData['inHtml'] = game.whoseTurnSymbol
        viewData['toLighten'] = toLighten

        if game.checkLocalWin() == en.PlayerSymbol.none:
            viewData['localGameEnded'] = False
            viewData['localBoardWinner'] = ''
        else:
            viewData['localGameEnded'] = True
            viewData['localBoardWinner'] = game.whoseTurnSymbol

        globalWinner = game.checkGlobalWin()

        if globalWinner != en.PlayerSymbol.none:
            viewData['globalGameEnded'] = True
            viewData['globalGameWinner'] = viewData['localBoardWinner']
            game.scoreTable[game.whoseTurnSymbol] += 1
            game.prepareNewRound()
        else:
            viewData['globalGameEnded'] = False
        for sid in room.clients:
            fsio.emit('actualizeView', viewData, room=sid)


def handleReceivedMessage(data, socketId):
    receivedMessageData = {
        'msg': data['msg']
    }
    room = getRoomClientIsConnectedTo(socketId)
    receivedMessageData['who'] = 'self'
    fsio.emit('receivedMessage', receivedMessageData, room=socketId)
    receivedMessageData['who'] = 'friend'
    for sid in room.clients:
        fsio.emit('receivedMessage', receivedMessageData, room=sid, include_self=False)


def handleJoinRoom(data, socketId):
    room = getRoomById(data['roomId'])
    joinData = {}
    gameActivated = False
    if room is not None:
        joinData['advancedMode'] = room.advancedMode
        joinData['playTime'] = room.playTime
        fsio.emit('joinRoom', joinData, room=socketId)
        room.connectClient(socketId)
        if len(room.whoseSocket) >= 2:
            if not room.isGameActive:
                gameActivated = True
                for sid in room.clients:
                    fsio.emit('startGame', room=sid)
                room.isGameActive = True
            else:
                fsio.emit('startGame', room=socketId)
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
    data = []
    for el in rooms:
        room = el['room']
        mode = 'casual'
        playTime = '-'
        if room.advancedMode:
            mode = 'advanced'
            playTime = str(room.playTime) + ' s'
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
