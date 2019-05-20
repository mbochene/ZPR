#!venv/bin/python3
import flask
import flask_socketio as fsio
import os
import sys
import event_handlers as evh
import eventlet as evt
import time
import clock

evt.monkey_patch()
APP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app')
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')
STATIC_DIR = os.path.join(APP_DIR, 'static')

app = flask.Flask(__name__, template_folder=TEMPLATE_DIR,
                  static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = 'tajemnica'
socketio = fsio.SocketIO(app)
namespace = None


@app.route('/')
def sessions():
    return flask.render_template('index.html', async_mode='eventlet')

@app.route('/shutdownServer')
def shutdown():
    socketio.stop()

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
def handleCreateRoom(data):
    evh.handleCreateRoom(data, flask.request.sid)


@socketio.on('joinRoom', namespace=namespace)
def handleJoinRoom(data):
    gameActivated, room = evh.handleJoinRoom(data, flask.request.sid)
    if gameActivated and room.advancedMode:
        socketio.start_background_task(target=clock.clock, room=room)


@socketio.on('leaveRoom', namespace=namespace)
def handleLeaveRoom():
    gameActivated, room = evh.handleLeaveRoom(flask.request.sid)
    if gameActivated and room.advancedMode:
        socketio.start_background_task(target=clock.clock, room=room)
