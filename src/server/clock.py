#!venv/bin/python3
import time
import flask_socketio as fsio
import config
import timer as tm



def clock(room):
    game = room.game
    timers = {
        room.clients[0]: tm.Timer(room.playTime),
        room.clients[1]: tm.Timer(room.playTime)
    }
    while True:
        if list(room.whoseSocket.keys()) != list(timers.keys()):
            return
        nowMovingSocketId = next((sid for sid, symbol in room.whoseSocket.items(
        ) if symbol == game.getWhoseTurn()), None)
        timer = timers.get(nowMovingSocketId)
        timer.start()
        time.sleep(0.3)
        timer.stop()
        if game.gameState != room.game.gameState:
            return
        if timer.check():
            globalWinner = next(
                (sid for sid, timer in timers.items() if sid != nowMovingSocketId), None)
            print(globalWinner)
            print(room.whoseSocket)
            print(room.whoseSocket.get(globalWinner))
            print(game.scoreTable.keys())
            winningSymbol = list(game.scoreTable.keys())[
                room.whoseSocket.get(globalWinner) - 1]
            viewData = {
                'id': 0,
                'toLighten': [0, 1, 2, 3, 4, 5, 6, 7, 8],
                'localGameEnded': True,
                'globalGameEnded': True,
                'localBoardWinner': winningSymbol,
                'globalGameWinner': winningSymbol,
            }
            clockData = {
                'playTime': room.playTime
            }
            game.prepareNewRound()
            with config.app.test_request_context():
                for sid in room.clients:
                    fsio.emit('actualizeView', viewData,
                              room=sid, namespace=None)
                    fsio.emit('actualizeClock', clockData,
                              room=sid, namespace=None)
                config.socketio.start_background_task(target=clock, room=room)
            return
        print(nowMovingSocketId + ': ' + str(timer.timeLeft))
