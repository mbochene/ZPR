#!/usr/bin/env python
import game
import session
import flask_socketio as fsio
class Room:
    def __init__(self, socketId, roomId):
        self.session = session.Session()
        self.roomId = roomId
        self.hostSocketId = socketId
    def addClient(self, socketId):
        self.session.connectClient(socketId)
    def removeClient(self, socketId):
        return self.session.disconnectClient(socketId)
    def isClientConnected(self, socketId):
        for sid in self.session.clients:
            if sid == socketId:
                return True
        return False