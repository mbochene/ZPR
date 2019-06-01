#!venv/bin/python3
## \file clock.py
#  Plik zawierjący definicję funkcji clock - uruchamianej w osobnym wątku do pomiaru czasu
#   pozostałego do końca gry.
import time
import flask_socketio as fsio
import config
import timer as tm

##  Wołana jako funkcja celu dla metody start_background_task na rzecz obiektu
# app (zdefiniowanego w pliku config.py) klasy flask.Flask <br>
# Funkcja odmierza czas dla grających użytkowników. Odmierzanie czasu opiera sie o funkcjonalność
# udostępnioną przez klasę timer.Timer. Obiekt odmierzajacy czas dla
# odpowiedniego gracza wybierany jest na podstawie id socketu gracza, do ktorego nalezy obecna tura.<br>
# W każdym obiegu pętli obiekt klasy timer.Timer aktualizuje pozostały czasu
# dla danego gracza, a wątek jest usypiany na 0.3 sekundy.
# Funkcja wykrywa sytuację, w której jeden z graczy przekroczy czas.
# Wówczas emitowane jest zdarzenie do użytkowników przebywającym w pokoju podanym
# jako argument wywołania funkcji.<br>
# Dodatkowo, funkcja przy kazdym obiegu pętli sprawdza, czy któryś z grających
# użytkowników nie opuścił pokoju (porównanie kluczy dla słowników timers oraz
# room.whoseSocket) lub czy gra nie została zakończona przed czasem -
# jeśli taka sytuacja wystąpiła, należy przerwać wątek.
# <br><br>
# @param room - pokój, dla którego odmierzany jest czas rozgrywki <br>
def clock(room):

    counter = 0
    game = room.game
    symbolList = sorted(list(game.scoreTable.keys()), reverse=True)
    scores = list(game.scoreTable.values())
    timers = {
        room.clients[0]: tm.Timer(room.playTime),
        room.clients[1]: tm.Timer(room.playTime)
    }
    nextMovingSocketId = next((sid for sid, symbol in room.whoseSocket.items(
    ) if symbol == game.getWhoseTurn()), None)
    while True:
        counter += 1
        # porównanie kluczy słowników timers oraz room.whoseSocket w celu
        # wykrycia sytuacji, w której jeden z grających użytkowników opuścił pokój
        nowMovingSocketId = nextMovingSocketId
        timer = timers.get(nowMovingSocketId)
        timer.start()
        time.sleep(0.3)
        timer.stop()
        # co 10 obieg pętli (0.3 sekundy) wysłanie zdarzenia synchronizującego
        # widok zegarów u użytkowników z ich stanem po stronie serwera
        if counter == 10:
            counter = 0
            with config.app.test_request_context():
                data = {
                    'timeLeft': timer.timeLeft,
                    'symbol': symbolList[
                        room.whoseSocket.get(nowMovingSocketId) - 1]
                }
                for sid in room.clients:
                    fsio.emit('actualizeClock', data, room=sid, namespace=None)
        # przerwanie wątku jeśli któryś z grających użytkowników opuści pokój (pierwszy warunek)
        # lub gdy gra skończy się przed czasem (drugi warunek) w instrukcji if.
        if list(room.whoseSocket.keys()) != list(timers.keys()) or scores != list(game.scoreTable.values()):
            return
        nextMovingSocketId = next((sid for sid, symbol in room.whoseSocket.items(
        ) if symbol == game.getWhoseTurn()), None)
        # dodatkowa synchronizacja zegarów wyświetlanych u użytkowników gdy nastąpi
        # zmiana tury.
        if nowMovingSocketId != nextMovingSocketId:
            with config.app.test_request_context():
                data = {
                    'symbol': symbolList[
                        room.whoseSocket.get(nowMovingSocketId) - 1],
                    'timeLeft': timers.get(nowMovingSocketId).timeLeft
                }
                for sid in room.clients:
                    fsio.emit('switchClock', data, room=sid, namespace=None)
        # zakończyła się rozgrywka (aktualnie grający użytkownik przekroczył czas)
        if timer.check():
            globalWinner = next(
                (sid for sid, timer in timers.items() if sid != nowMovingSocketId), None)
            winningSymbol = symbolList[
                room.whoseSocket.get(globalWinner) - 1]
            game.scoreTable[winningSymbol] += 1
            game.prepareNewRound()
            viewData = {
                'id': 0,
                'toLighten': [0, 1, 2, 3, 4, 5, 6, 7, 8],
                'localGameEnded': True,
                'globalGameEnded': True,
                'localBoardWinner': winningSymbol,
                'globalBoardWinner': winningSymbol,
            }
            print(game.scoreTable)
            with config.app.test_request_context():
                for sid in room.clients:
                    fsio.emit('actualizeView', viewData,
                              room=sid, namespace=None)
                    fsio.emit('startGame',
                              room=sid, namespace=None)
                config.socketio.start_background_task(target=clock, room=room)
            return
