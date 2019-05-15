#!/usr/bin/env python
import flask_socketio as fsio
import engine as en
import room
import string
import random

rooms = []


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def getRoomClientIsConnectedTo(socketId):
    for el in rooms:
        if el['room'].isClientConnected(socketId):
            return el['room']
    return None


def getRoomById(roomId):
    for el in rooms:
        if el['room'].roomId == roomId:
            return el['room']
    return None


def handleCreateRoom(socketId):
    roomId = str(socketId)[-2:] + id_generator(4) + str(socketId)[:2]
    newRoom = room.Room(socketId, roomId)
    rooms.append({'socketId': socketId, 'room': newRoom})
    data = {
        'roomId': roomId,
        'roomInfo': 'po prostu rum',
        'status': ''
    }
    handleJoinRoom(data, socketId)
    fsio.emit('createRoom', data, broadcast=True)


def handleClickedField(data, socketId):
    room = getRoomClientIsConnectedTo(socketId)
    if room is None:
        return
    game = room.session.game
    if room.session.whoseSocket.get(socketId) is None or room.session.whoseSocket.get(socketId) != game.getWhoseTurn():
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
            game.scoreTable[game.whoseTurnSymbol] += 1
            game.prepareNewRound()
        else:
            data['globalGameEnded'] = False

        for sid in room.session.clients:
            fsio.emit('actualizeView', data, room=sid)


def handleReceivedMessage(data, socketId):
    room = getRoomClientIsConnectedTo(socketId)
    data['who'] = 'self'
    fsio.emit('receivedMessage', data, room=socketId)
    data['who'] = 'friend'
    for sid in room.session.clients:
        fsio.emit('receivedMessage', data, room=sid, include_self=False)


def handleJoinRoom(data, socketId):
    room = getRoomById(data['roomId'])
    if room is not None:
        data['status'] = 'JOINED_ROOM'
        fsio.emit('joinRoom', data, room=socketId)
        room.addClient(socketId)
        if len(room.session.whoseSocket) >= 2:
            if not room.session.isGameActive:
                for sid in room.session.clients:
                    fsio.emit('startGame', room=sid)
                room.session.isGameActive = True
            else:
                fsio.emit('startGame', data, room=socketId)
    else:
        data['status'] = 'INVALID_ROOM_ID'
        fsio.emit('joinRoom', data, room=socketId)


def handleLeaveRoom(socketId):
    room = getRoomClientIsConnectedTo(socketId)
    if room is not None:
        if room.removeClient(socketId):
            for sid in room.session.clients:
                fsio.emit('stopGame', room=sid)
            if room.session.numberOfConnectedClients >= 2:
                room.session.isGameActive = True
                for sid in room.session.clients:
                    fsio.emit('startGame', room=sid)
    fsio.emit('stopGame', room=socketId)
    fsio.emit('leaveRoom', room=socketId)


def handleConnection(socketId):
    print(socketId + " connected")
    data = []
    for el in rooms:
        data.append({'roomInfo': 'po prostu rum', 'roomId': el['room'].roomId})
    fsio.emit('initializeRoomsList', data, room=socketId)


def handleDisconnection(socketId):
    handleLeaveRoom(socketId)
    fsio.emit('disconnect', room=socketId)
