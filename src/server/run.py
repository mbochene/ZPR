#!venv/bin/python3
## \file run.py
#  Plik główny - uruchamiający serwer
import config
import threading
import eventlet as evt
evt.monkey_patch()

if __name__ == '__main__':
    config.socketio.run(config.app, host='0.0.0.0', debug=True)
