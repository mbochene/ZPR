#!/usr/bin/env python
import flask
import flask_socketio as fsio
import os
import event_handlers as evh

appDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app')
templateDir = os.path.join(appDir, 'templates')
staticDir = os.path.join(appDir, 'static')

app = flask.Flask(__name__, template_folder=templateDir,
                  static_folder=staticDir)
app.config['SECRET_KEY'] = 'tajemnica'
socketio = fsio.SocketIO(app)

namespace = None


@app.route('/')
def sessions():
    return flask.render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('clickedField', namespace=namespace)
def handleClick(data):
    evh.handleClickedField(data, flask.request.sid)


@socketio.on('msgSent', namespace=namespace)
def handleMessage(data):
    evh.handleReceivedMessage(data, flask.request.sid)


@socketio.on('connect', namespace=namespace)
def handleConnect():
    evh.handleConnection(flask.request.sid)


@socketio.on('disconnect', namespace=namespace)
def handleDisconnect():
    evh.handleDisconnection(flask.request.sid)

@socketio.on('createRoom', namespace=namespace)
def handleCreateRoom():
    evh.handleCreateRoom(flask.request.sid)

@socketio.on('joinRoom', namespace=namespace)
def handleJoinRoom(data):
    evh.handleJoinRoom(data, flask.request.sid)

@socketio.on('leaveRoom', namespace=namespace)
def handleLeaveRoom():
    evh.handleLeaveRoom(flask.request.sid)