#!/usr/bin/env python
import os, sys, inspect
import pytest
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from game import * 
from event_handlers import *
from session import *
from config import *

namespace=None

def testNumberOfConnectedClientsAfterConnection():
    testClient=socketio.test_client(app, namespace)
    assert session.numberOfConnectedClients == 1
    testClient.disconnect()
    
def testFirstConnectedPlayerBecomesPlayer1():
    testClient=socketio.test_client(app, namespace)
    assert session.whoseSocket[testClient.sid] == 1
    testClient.disconnect()

def testSecondConnectedPlayerBecomesPlayer2():
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    assert session.whoseSocket[testClient2.sid] == 2
    testClient1.disconnect()
    testClient2.disconnect()

def testSecondConnectedPlayerBecomesPlayer1AfterFirstDisconnection():
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    testClient1.disconnect()
    assert session.whoseSocket[testClient2.sid] == 1
    testClient2.disconnect()

def testThirdConnectedPlayerIsNotPresentInSocketsDictionary():
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    testClient3=socketio.test_client(app, namespace)
    assert session.whoseSocket.get(testClient3.sid) == None
    testClient1.disconnect()
    testClient2.disconnect()
    testClient3.disconnect()

def testGameIsActiveAfterSecondPlayerConnection():
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    assert session.isGameActive
    testClient1.disconnect()
    testClient2.disconnect()

def testGameIsNotActiveAfterOneOfTwoPlayersDisconnection():
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    testClient1.disconnect()
    assert not session.isGameActive
    testClient2.disconnect()

parameters = []
for i in range(9):
        for j in range(9):
                parameters.append((str(i)+str(j), [j]))
                
@pytest.mark.parametrize('id, result',
                                parameters
                         )
def testClickOnSquareActivatesProperBoard(id, result):
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    data = {
            'id': id,
            'inHtml': '',
            'toLighten': [],
            'localGameEnded': False,
            'localBoardWinner': '',
            'globalGameEnded': False
    }
    testClient1.emit('clickedField', data)
    resp=testClient1.get_received(namespace)
    assert resp[len(resp)-1]['args'][0][u'toLighten'] == result
    testClient1.disconnect()
    testClient2.disconnect()

parameters=[
        (['06', '07', '08'],
        ['60', '70', '80']),
        (['03', '04', '05'],
         ['30', '40', '50'])
]


@pytest.mark.parametrize('client1Moves, client2Moves',
                         parameters
                         )
def testClickOnSquareMovingOponentToAlreadyWonBoardActivatesAllBoards(client1Moves, client2Moves):
    result=[1,2,3,4,5,6,7,8]
    testClient1=socketio.test_client(app, namespace)
    testClient2=socketio.test_client(app, namespace)
    data = {
            'id': '',
            'inHtml': '',
            'toLighten': [],
            'localGameEnded': False,
            'localBoardWinner': '',
            'globalGameEnded': False
    }
    for i in range(len(client1Moves)):
        data['id']=client1Moves[i]
        testClient1.emit('clickedField', data)
        data['id']=client2Moves[i]
        testClient2.emit('clickedField', data)
    resp=testClient2.get_received(namespace)
    assert resp[len(resp)-1]['args'][0][u'toLighten']==result
    testClient1.disconnect()
    testClient2.disconnect()