import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from game import * 
from event_handlers import *
from session import *
from config import *

namespace=None

def testNumberOfConnectedClientsAfterConnection():
    test_client=socketio.test_client(app, namespace)
    assert session.numberOfConnectedClients == 1
    test_client.disconnect()
    
def testFirstConnectedPlayerBecomesPlayer1():
    test_client=socketio.test_client(app, namespace)
    assert session.whoseSocket[test_client.sid] == 1
    test_client.disconnect()

def testSecondConnectedPlayerBecomesPlayer2():
    test_client1=socketio.test_client(app, namespace)
    test_client2=socketio.test_client(app, namespace)
    assert session.whoseSocket[test_client2.sid] == 2
    test_client1.disconnect()
    test_client2.disconnect()

def testSecondConnectedPlayerBecomesPlayer1AfterFirstDisconnection():
    test_client1=socketio.test_client(app, namespace)
    test_client2=socketio.test_client(app, namespace)
    test_client1.disconnect()
    assert session.whoseSocket[test_client2.sid] == 1
    test_client2.disconnect()

def testThirdConnectedPlayerIsNotPresentInSocketsDictionary():
    test_client1=socketio.test_client(app, namespace)
    test_client2=socketio.test_client(app, namespace)
    test_client3=socketio.test_client(app, namespace)
    assert session.whoseSocket.get(test_client3.sid) == None
    test_client1.disconnect()
    test_client2.disconnect()
    test_client3.disconnect()

def testGameIsActiveAfterSecondPlayerConnection():
    test_client1=socketio.test_client(app, namespace)
    test_client2=socketio.test_client(app, namespace)
    assert session.isGameActive
    test_client1.disconnect()
    test_client2.disconnect()

def testGameIsNotActiveAfterOneOfTwoPlayersDisconnection():
    test_client1=socketio.test_client(app, namespace)
    test_client2=socketio.test_client(app, namespace)
    test_client1.disconnect()
    assert not session.isGameActive
    test_client2.disconnect()

def testClickOnRightTopCornerOfSquareLightensRightTopBoard():
    test_client1=socketio.test_client(app, namespace)
    test_client2=socketio.test_client(app, namespace)
    data = {
            'id': '08',
            'inHtml': '',
            'toLighten': [],
            'localGameEnded': False,
            'localBoardWinner': '',
            'globalGameEnded': False
    }
    test_client1.emit('clickedField', data)
    resp=test_client1.get_received(namespace)
    assert resp[1]['args'][0][u'toLighten'] == [8]
    test_client1.disconnect()
    test_client2.disconnect()

