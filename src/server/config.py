#!C:\Users\sergi\AppData\Local\Programs\Python\Python37-32\python.exe
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import eventlet
import os

appDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app')
templateDir = os.path.join(appDir, 'templates')
staticDir = os.path.join(appDir, 'static')

app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)
app.config['SECRET_KEY'] = 'tajemnica'
socketio = SocketIO(app)

whoNow = 'X'
playNowHere = 1

@app.route('/')
def sessions():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('test', namespace='/test')
def handleTest():
    print('tested')


@socketio.on('clickedField', namespace='/test')
def handleClickedField(data):
    global whoNow
    global playNowHere
    id = int(data['id'])
    if(id // 10 == playNowHere):
        inHtml = data['inHtml']
        if(inHtml == ''):
            data['previouslyPlayed'] = playNowHere
            inHtml = whoNow
            if(whoNow == 'X'):
                whoNow = 'O'
            else:
                whoNow = 'X'
            playNowHere = id % 10
        data['inHtml'] = inHtml
        data['playNowHere'] = playNowHere
    emit('respondToClickedField', data, broadcast=True)


@socketio.on('msgSent', namespace='/test')
def handleReceivedMessage(msg):
    print(msg)
    emit('respondToReceivedMessage', msg, broadcast=True)


