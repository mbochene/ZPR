#!/usr/bin/env python
import game

class Session:
    def __init__(self):
        self.numberOfConnectedClients = 0
        self.clients = []
        self.whoseSocket = {}
        self.game = game.Game()
        self.isGameActive = False

    def connectClient(self, socketId):
        self.numberOfConnectedClients += 1
        self.clients.append(socketId)
        dictLength = len(self.whoseSocket)
        if dictLength < 2:
            self.whoseSocket[socketId] = dictLength + 1

    # zwraca true jesli odlacza sie jeden z grajacych; w.p.p. zwraca false
    def disconnectClient(self, socketId):
        self.numberOfConnectedClients -= 1
        self.clients.remove(socketId)
        if self.whoseSocket.get(socketId) != None:
            self.isGameActive = False
            self.game.prepareNewGame()
            self.whoseSocket.pop(socketId)
            for socket in self.whoseSocket:             # jak 1 gracz sie odlaczy, to 2 gracz ma stac sie 1 graczem
                # dodac emita restartujacego gre
                self.whoseSocket[socket] = 1
            if self.numberOfConnectedClients >= 2:
                self.whoseSocket[self.clients[1]] = 2
            return True
        return False

    def getNumberOfConnectedClients(self):
        return self.numberOfConnectedClients
