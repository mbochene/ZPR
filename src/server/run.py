#!/usr/bin/env python
from config import socketio, app
import threading

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', debug=True)
