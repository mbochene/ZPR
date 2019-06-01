#!venv/bin/python3
## \file config.py
#  Plik zawierający konfigurację serwera (utworzenie obiektu klasy flask.Flask,
#  ustalenie ścieżek do istotnych katalogów, a także definicje funkcji
#  obsługujących poszczególne żądania przesyłane przez klienta)
import flask
import flask_socketio as fsio
import os
import sys
import event_handlers as evh
import time
import clock

## Bezwzględna ścieżka do katalogu zawierającego pliki dla klienta
APP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app')
## Bezwzględna ścieżka do katalogu zawierającego opis strony w języku HTML
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')
## Bezwzględna ścieżka do katalogu zawierającego skrypty w języku JavaScript (STATIC_DIR/js),
#  opis stylów w CSS (STATIC_DIR/css) oraz grafikę (STATIC_DIR/img).
STATIC_DIR = os.path.join(APP_DIR, 'static')
## centralny obiekt aplikacji (instancja klasy flask.Flask) - odpowiada za konfigurację serwera.
app = flask.Flask(__name__, template_folder=TEMPLATE_DIR,
                  static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = 'tajemnica'
## serwer (obiekt klasy flask_socketio.SocketIO)
socketio = fsio.SocketIO(app)
namespace = None

## domyślne przekierowanie na stronę z widokiem gry
@app.route('/')
def sessions():
    return flask.render_template('index.html', async_mode='eventlet')


## wyłączenie serwera przechodząc pod adres SERVER_IP_ADDR:5000/shutdownServer
@app.route('/shutdownServer')
def shutdown():
    socketio.stop()

@socketio.on('clickedField', namespace=namespace)
## funkcja obsługująca żądanie 'clickedField' przesłane przez klienta.
#  @param data - dane zapisane w słowniku (id klikniętego pola)
def handleClick(data):
    evh.handleClickedField(data, flask.request.sid)

@socketio.on('msgSent', namespace=namespace)
## funkcja obsługująca żądanie 'msgSent' przesłane przez klienta.
#  @param data - dane zapisane w słowniku (wysłana na czacie treść wiadomości)
def handleMessage(data):
    evh.handleReceivedMessage(data, flask.request.sid)


@socketio.on('connect', namespace=namespace)
## funkcja obsługująca żądanie 'connect' przesłane przez klienta.
def handleConnect():
    evh.handleConnection(flask.request.sid)


@socketio.on('disconnect', namespace=namespace)
## funkcja obsługująca żądanie 'disconnect' przesłane przez klienta.
def handleDisconnect():
    evh.handleDisconnection(flask.request.sid)


@socketio.on('createRoom', namespace=namespace)
## funkcja obsługująca żądanie 'createRoom' przesłane przez klienta.
#  @param data - dane zapisane w słowniku (nazwa pokoju, tryb rozgrywki, czas gry)
def handleCreateRoom(data):
    evh.handleCreateRoom(data, flask.request.sid)


@socketio.on('joinRoom', namespace=namespace)
## funkcja obsługująca żądanie 'joinRoom' przesłane przez klienta.
#  uruchamia w tle wątek odmierzający czas dla graczy.
#  @param data - dane zapisane w słowniku (id pokoju)
def handleJoinRoom(data):
    gameActivated, room = evh.handleJoinRoom(data, flask.request.sid)
    if gameActivated and room.advancedMode:
        socketio.start_background_task(target=clock.clock, room=room)


@socketio.on('leaveRoom', namespace=namespace)
## funkcja obsługująca żądanie 'leaveRoom' przesłane przez klienta.
def handleLeaveRoom():
    gameActivated, room = evh.handleLeaveRoom(flask.request.sid)
    if gameActivated and room.advancedMode:
        socketio.start_background_task(target=clock.clock, room=room)
