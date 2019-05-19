#!venv/bin/python3
from config import socketio, app
import threading

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
