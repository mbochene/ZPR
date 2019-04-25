#!/usr/bin/env python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import eventlet
import os
import event_handlers
appDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app')
templateDir = os.path.join(appDir, 'templates')
staticDir = os.path.join(appDir, 'static')

app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)
app.config['SECRET_KEY'] = 'tajemnica'
socketio = SocketIO(app)

whoNow = 'X'
playNowHere = 1
namespace=None

@app.route('/')
def sessions():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('clickedField', namespace=namespace)
def handleClick(data):
    socketId = request.sid
    event_handlers.handleClickedField(data, socketId)


@socketio.on('msgSent', namespace=namespace)
def handleMessage(data):
    socketId = request.sid
    event_handlers.handleReceivedMessage(data, socketId)


@socketio.on('connect', namespace=namespace)
def handleConnect():
    socketId = request.sid
    event_handlers.handleConnection(socketId)


@socketio.on('disconnect', namespace=namespace)
def handleDisconnect():
    socketId = request.sid
    event_handlers.handleDisconnection(socketId)
