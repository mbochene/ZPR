#!C:\Users\sergi\AppData\Local\Programs\Python\Python37-32\python.exe

from config import socketio, app

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
