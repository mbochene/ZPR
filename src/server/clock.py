#!venv/bin/python3
import time
import flask_socketio as fsio
import config
import timer as tm


def clock(room):
    counter = 0
    game = room.game
    timers = {
        room.clients[0]: tm.Timer(room.playTime),
        room.clients[1]: tm.Timer(room.playTime)
    }
    symbolList = sorted(list(game.scoreTable.keys()), reverse=True)
    nextMovingSocketId = next((sid for sid, symbol in room.whoseSocket.items(
    ) if symbol == game.getWhoseTurn()), None)
    while True:
        counter += 1
        if list(room.whoseSocket.keys()) != list(timers.keys()):
            return
        nowMovingSocketId = nextMovingSocketId
        timer = timers.get(nowMovingSocketId)
        timer.start()
        time.sleep(0.25)
        timer.stop()
        if counter == 12:
            counter = 0
            with config.app.test_request_context():
                data = {
                    'timeLeft': timer.timeLeft,
                    'symbol': symbolList[
                        room.whoseSocket.get(nowMovingSocketId) - 1]
                }
                for sid in room.clients:
                    fsio.emit('actualizeClock', data, room=sid, namespace=None)
        nextMovingSocketId = next((sid for sid, symbol in room.whoseSocket.items(
        ) if symbol == game.getWhoseTurn()), None)
        if nowMovingSocketId != nextMovingSocketId:
            with config.app.test_request_context():
                data = {
                    'nextSymbol': symbolList[
                        room.whoseSocket.get(nextMovingSocketId) - 1],
                    'nextTimeLeft': timers.get(nextMovingSocketId).timeLeft
                }
                for sid in room.clients:
                    fsio.emit('switchClock', data, room=sid, namespace=None)

        if game.gameState != room.game.gameState:
            return
        if timer.check():
            globalWinner = next(
                (sid for sid, timer in timers.items() if sid != nowMovingSocketId), None)
            winningSymbol = symbolList[
                room.whoseSocket.get(globalWinner) - 1]
            viewData = {
                'id': 0,
                'toLighten': [0, 1, 2, 3, 4, 5, 6, 7, 8],
                'localGameEnded': True,
                'globalGameEnded': True,
                'localBoardWinner': winningSymbol,
                'globalGameWinner': winningSymbol,
            }
            game.prepareNewRound()
            with config.app.test_request_context():
                for sid in room.clients:
                    fsio.emit('actualizeView', viewData,
                              room=sid, namespace=None)
                    fsio.emit('startGame',
                              room=sid, namespace=None)
                config.socketio.start_background_task(target=clock, room=room)
            return
        print(nowMovingSocketId + ': ' + str(timer.timeLeft))
