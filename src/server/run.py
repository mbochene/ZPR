#!venv/bin/python3
## \file run.py
#  Plik główny - uruchamiający serwer
import config
import threading
if __name__ == '__main__':
    config.socketio.run(config.app, host='0.0.0.0', debug=True)
