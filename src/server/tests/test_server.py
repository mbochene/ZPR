#!venv/bin/python3
import pytest
import os
import sys
import inspect
#os.chdir(os.path.dirname(os.path.realpath(__file__)))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(
inspect.getfile(inspect.currentframe()))))
sys.path.insert(0, parent_dir)
import config
import event_handlers as evh
import room
import engine

namespace = None


def testJoinRoom():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
    })
    resp = testClient2.get_received(namespace)
    room = evh.getRoomById(roomId)
    assert resp[len(resp) - 2]['args'][0][u'roomId'] == roomId
    assert resp[len(resp) - 2]['args'][0][u'advancedMode'] == advancedMode
    assert resp[len(resp) - 2]['args'][0][u'playTime'] == playTime
    assert room.numberOfConnectedClients == 2
    testClient.disconnect()
    testClient2.disconnect()


def testPlayerWhoJoinsRoomFirstBecomesPlayer1():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    room = evh.getRoomById(roomId)
    assert room.whoseSocket[testClient.sid] == 1
    testClient.disconnect()
    testClient2.disconnect()


def testPlayerWhoJoinsRoomSecondBecomesPlayer2():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    room = evh.getRoomById(roomId)
    assert room.whoseSocket[testClient2.sid] == 2
    testClient.disconnect()
    testClient2.disconnect()


def testSecondlyJoinedPlayerBecomesPlayer1AfterFirstLeaves():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    room = evh.getRoomById(roomId)
    testClient.disconnect()
    assert room.whoseSocket[testClient2.sid] == 1
    testClient2.disconnect()


def testThirdConnectedPlayerIsNotPresentInSocketsDictionary():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    testClient3 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    testClient3.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    room = evh.getRoomById(roomId)
    assert room.whoseSocket.get(testClient3.sid) is None
    testClient.disconnect()
    testClient2.disconnect()
    testClient3.disconnect()


def testGameIsActiveWhenSecondPlayerJoinsRoom():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    room = evh.getRoomById(roomId)
    assert room.isGameActive
    testClient.disconnect()
    testClient2.disconnect()


def testGameIsNotActiveWhenOneOfTwoPlayersLeavesRoom():
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    room = evh.getRoomById(roomId)
    testClient.disconnect()
    assert not room.isGameActive
    testClient2.disconnect()


parameters = []
for i in range(9):
    for j in range(9):
        parameters.append((str(i) + str(j), [j]))


@pytest.mark.parametrize('id, result',
                         parameters
                         )
def testClickOnSquareActivatesProperBoard(id, result):
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })

    data = {
        'id': id
    }
    testClient.emit('clickedField', data)
    resp = testClient.get_received(namespace)
    assert resp[len(resp) - 1]['args'][0][u'toLighten'] == result
    testClient.disconnect()
    testClient2.disconnect()


parameters = [
    (['06', '07', '08'],
     ['60', '70', '80']),
    (['03', '04', '05'],
     ['30', '40', '50'])
]


@pytest.mark.parametrize('client1Moves, client2Moves',
                         parameters
                         )
def testClickOnSquareMovingOponentToAlreadyWonBoardActivatesAllBoards(client1Moves, client2Moves):
    result = [1, 2, 3, 4, 5, 6, 7, 8]
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    data = {
        'id': ''
    }
    for i in range(len(client1Moves)):
        data['id'] = client1Moves[i]
        testClient.emit('clickedField', data)
        data['id'] = client2Moves[i]
        testClient2.emit('clickedField', data)
    resp = testClient2.get_received(namespace)
    assert resp[len(resp) - 1]['args'][0][u'toLighten'] == result
    testClient.disconnect()
    testClient2.disconnect()


parameters = [
    (['60', '70', '80'],
     ['07', '08', '06']),
    (['30', '40', '50'],
     ['04', '05', '03'])
]


@pytest.mark.parametrize('client1Moves, client2Moves',
                         parameters
                         )
def testCheckLocalWin(client1Moves, client2Moves):
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    room = evh.getRoomById(roomId)
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    data = {
        'id': ''
    }
    for i in range(len(client1Moves)):
        data['id'] = client1Moves[i]
        testClient.emit('clickedField', data)
        data['id'] = client2Moves[i]
        testClient2.emit('clickedField', data)
    assert room.game.playerSymbol[room.game.checkLocalWin()].upper() == 'O'
    assert room.game.isBoardNotPlayable(int(client2Moves[0][0]))
    resp = testClient2.get_received(namespace)
    testClient.disconnect()
    testClient2.disconnect()


parameters = [
    (['60', '70', '80', '61', '31', '41', '52', '32', '42'],
     ['07', '08', '06', '13', '14', '15', '23', '24', '25']),
    (['03', '13', '23', '04', '64', '74', '85', '05', '15'],
     ['31', '32', '30', '46', '47', '48', '50', '51', '52'])
]


@pytest.mark.parametrize('client1Moves, client2Moves',
                         parameters
                         )
def testCheckGlobalWin(client1Moves, client2Moves):
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    room = evh.getRoomById(roomId)
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    data = {
        'id': ''
    }
    for i in range(len(client1Moves)):
        data['id'] = client1Moves[i]
        testClient.emit('clickedField', data)
        data['id'] = client2Moves[i]
        testClient2.emit('clickedField', data)
    assert room.game.scoreTable['O'] == 1
    resp = testClient2.get_received(namespace)
    testClient.disconnect()
    testClient2.disconnect()



parameters = [
    (['08', '80', '55','02','20','77','06','60','44','01','10','03'],
     ['88', '05', '50','22','07','70','66','04','40','11','00'])
]


@pytest.mark.parametrize('client1Moves, client2Moves',
                         parameters
                         )
def testCheckDraw(client1Moves, client2Moves):
    testClient = config.socketio.test_client(config.app, namespace)
    testClient2 = config.socketio.test_client(config.app, namespace)
    roomName = 'roomname'
    advancedMode = False
    playTime = 0
    testClient.emit('createRoom', {
        'roomName': 'roomname',
        'advancedMode': False,
        'playTime': 0,
    })
    resp = testClient.get_received(namespace)
    roomId = resp[len(resp) - 1]['args'][0][u'roomId']
    room = evh.getRoomById(roomId)
    testClient2.emit('joinRoom', {
        'roomId': roomId,
        'advancedMode': '',
        'playTime': '',
        'status': ''
    })
    data = {
        'id': ''
    }
    for i in range(len(client2Moves)):
        data['id'] = client1Moves[i]
        testClient.emit('clickedField', data)
        data['id'] = client2Moves[i]
        testClient2.emit('clickedField', data)
    data['id'] = client1Moves[len(client1Moves) - 1]
    testClient.emit('clickedField', data)
    assert room.game.playerSymbol[room.game.checkLocalWin()].upper() == 'NONE'
    assert room.game.isBoardNotPlayable(int(client1Moves[0][0]))
    resp = testClient2.get_received(namespace)
    testClient.disconnect()
    testClient2.disconnect()
