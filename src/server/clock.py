#!venv/bin/python3
import time
import flask_socketio as fsio
import config
import timer as tm

##  clock - wołana jako funkcja celu dla metody start_background_task
#                  na rzecz obiektu app (zdefiniowanego w pliku config.py)
#                  klasy flask.Flask
# @param room - pokój, dla którego odmierzany jest czas rozgrywki <br>
# <dl><dt style="font-weight: bold;">funkcjonalność:</dt><br>
# <dd>Funkcja odmierza czas dla grających użytkowników.<br>
# Odmierzanie czasu opiera sie o funkcjonalność udostępnioną przez obiekty
# klasy timer.Timer. Obiekt odmierzajacy czas dla odpowiedniego gracza wybierany
# jest na podstawie id socketu gracza, do ktorego nalezy obecna tura.<br>
# W każdym obiegu pętli obiekt klasy timer.Timer aktualizuje pozostały czasu
# dla danego gracza, a wątek jest usypiany na 0.3 sekundy.
# Funkcja wykrywa sytuację, w której jeden z graczy przekroczy czas.
# Wówczas emitowane jest zdarzenie do użytkowników przebywającym w pokoju podanym
# jako argument wywołania funkcji.<br>
# Dodatkowo, funkcja przy kazdym obiegu pętli sprawdza, czy któryś z grających
# użytkowników nie opuścił pokoju (porównanie kluczy dla słowników timers oraz
# room.whoseSocket) lub czy gra nie została zakończona przed czasem -
# jeśli taka sytuacja wystąpiła, należy przerwać wątek.
# </dd></dl> <br><br>
## <span style="font-size: 20px;"><b>zmienne lokalne:</b></span><br><br>
## <b>counter</b> - mierzy ilośc obiegów pętli. Co 10 obieg pętli (3 sekundy) emitowane
#           jest zdarzenie 'actualizeClock' do wszystkich użytkowników
#           połączonych z pokojem, aby zapewnić synchronizację widoku zegarów
#           u klienta z ich stanem po stronie serwera.
## game - referencja do obiektu klasy game.Game (atrybut obiektu room)
## symbolList - posortowana lista symboli - wykorzystywana w pętli w celu
#              szybkiego dostępu do odpowiedniego symbolu w przypadku wysyłania
#              danych o stanie zegara do klienta.
## timers - słownik zawierający obiekty klasy timer.Timer. Kluczami są id socket'ów
#          grajacych użytkowników.
## nowMovingSocketId - id socket'u  użytkownika, dla którego aktualnie
#                     odmierzany jest czas.
## nextMovingSocketId - id socket'u użytkownika, dla którego czas odmierzany będzie
#                      po uśpieniu wątku na 0.3 sekundy. Ta zmienna porównywana
#                      jest w każdym obiegu pętli ze zmienną nowMovingSocketId.
#                      Jeśli zmienne te się różnią (nastąpiła zmiana tury),
#                      wówczas emitowane jest zdarzenie 'actualizeClock'
#                      w celu synchronizacji widoku zegarów u użytkownika.
## scores - tablica wyników. W każdym obiegu pętli porównywana jest z aktualną
#           tablicą wyników. Jeśli tablice te się różnią, wówczas wątek jest
#           przerywany.

def clock(room):

    counter = 0
    game = room.game
    symbolList = sorted(list(game.scoreTable.keys()), reverse=True)
    timers = {
        room.clients[0]: tm.Timer(room.playTime),
        room.clients[1]: tm.Timer(room.playTime)
    }
    #engineSymbols = [{client: engineSymbol} for client in room.whoseSocket.keys() for engineSymbol
    #                 in playerSymbol if symbolList[room.whoseSocket.get(client) - 1] == playerSymbol.get(engineSymbol)]
    scores = list(game.scoreTable.values())
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
        if list(room.whoseSocket.keys()) != list(timers.keys()) or scores != list(game.scoreTable.values()):
            return
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
        # zakończyła się rozgrywka (aktualnie grający użytkownik przekroczył czas)
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
            game.scoreTable[winningSymbol] += 1
            game.prepareNewRound()
            with config.app.test_request_context():
                for sid in room.clients:
                    fsio.emit('actualizeView', viewData,
                              room=sid, namespace=None)
                    fsio.emit('startGame',
                              room=sid, namespace=None)
                config.socketio.start_background_task(target=clock, room=room)
            return
