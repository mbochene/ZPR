#!venv/bin/python3
import config
import threading

if __name__ == '__main__':
    config.socketio.run(config.app, host='0.0.0.0', debug=True)
