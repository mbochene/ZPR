#!venv/bin/python3
## \file event_handlers.py
#  Plik zawierający funkcje obsługujące żądania wysyłane przez klientów.
import flask_socketio as fsio
import room
import string
import random

## Słownik, którego kluczami są id hostów pokoju,a wartościami obiekty klasy room.Room
rooms = []

## Generuje losowy identyfikator (roomId)<br>
#  Zwraca:<br>
#  Losowo wygenerwoany ciąg znaków o długości size (string)
#  @param size - długość losowanego ciągu znaków; domyślnie 6(int)
#  @param chars - znaki, z których losowany jest ciąg znaków; domyślnie duże litery i cyfry
def generateRoomId(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

## Wyszukuje pokój, w którym przebywa klient o podanym id socketu<br>
#  Zwraca:<br>
#  obiekt klasy room.Room jeśli klient przebywa w którymś z pokojów ze słownika 'rooms'<br>
#  None w przeciwnym przypadku
#  @param socketId - id socketu klienta
def getRoomClientIsConnectedTo(socketId):
    for el in rooms:
        if el['room'].isClientConnected(socketId):
            return el['room']
    return None

## Wyszukuje pokoju o podanym id w słowniku pokojów ('rooms')<br>
#  Zwraca:
#  obiekt klasy room.Room o podanym roomId jeśli taki pokój znajduje się w słowniku 'rooms'<br>
#  None w przeciwnym przypadku
#  @param roomId - id wyszukiwanego pokoju
def getRoomById(roomId):
    for el in rooms:
        if el['room'].id == roomId:
            return el['room']
    return None

## Obsługuje żądanie utworzenia pokoju przez klienta
#  generuje id pokoju przy z wykorzystaniem funkcji generateRoomId, nastepnie
#  tworzy pokój o trybie rozgrywki wskazanym przez klienta, łączy go z pokojem
#  i wysyła informację o utworzeniu pokoju do wszystkich klientów połączonych z serwerem.
#  @param data - słownik, w kórym klient przesyła dane niezbędne do utworzenia pokoju
#  (nazwa pokoju(string), tryb rozgrywki(bool) oraz czas gry(int) - wartość
#  ignorowana gdy tryb rozgrywki = false - standardowa gra)
#  @param socketId - id socketu, z którego zostało wysłane żądanie utworzenia pokoju
def handleCreateRoom(data, socketId):
    roomId = str(socketId)[-2:] + generateRoomId() + str(socketId)[:2]
    newRoom = room.Room(
        socketId, roomId, data['roomName'], data['advancedMode'], int(data['playTime']))
    rooms.append({'socketId': socketId, 'room': newRoom})
    mode = 'casual'
    playTime = '-'
    if data['advancedMode']:
        mode = 'advanced'
        playTime = str(data['playTime']) + ' s'
    createData = {
        'roomId': roomId,
        'roomName': data['roomName'],
        'mode': mode,
        'playTime': playTime
    }
    joinData = {
        'roomId': roomId
    }
    handleJoinRoom(joinData, socketId)
    fsio.emit('createRoom', createData, broadcast=True)


## Obsługuje żądanie zajęcia pola na planszy przez klienta
#  Weryfikuje czy klient, który wysyla żądanie jest w słowniku obecnie grających
#  klientów. Następnie sprawdzana jest poprawność ruchu (czy ruch jest możliwy do wykonania).
#  Jeśli wszystkie warunki zostaną spełnione, do użytkownika przesyłana jest informacja
#  o tym, które pola należy podświetlić, jaki symbol wpisać w kliknięte pole,
#  czy zakońćzyła się rozgrywka na planszy lokalnej, na globalnej oraz ewentualnie
#  informację o tym, kto wygrał (lub że wystąpił remis).
#  @param data - słownik, w kórym klient przesyła id pola, które chce zająć
#  @param socketId - id socketu, z którego zostało wysłane żądanie kliknięcia pola
def handleClickedField(data, socketId):
    viewData = {
        'id': data['id']
    }
    room = getRoomClientIsConnectedTo(socketId)
    # jeśli klient nie przebywał w żadnym pokoju - przerwij obsługę zdarzenia
    # (po stronie użytkownika nie powinno się nic zmienić)
    if room is None:
        return
    game = room.game
    # jeśli id socketu klienta wysyłającego żadanie nie znajduje się w słowniku aktualnie
    # grających klientów, przerwij obsługę zdarzenia (nic nie powinno się zmienić)
    if room.whoseSocket.get(socketId) is None or room.whoseSocket.get(socketId) != game.getWhoseTurn():
        return
    # inicjacja tablicy z id plansz, które należy podświetlić.
    toLighten = []
    # id klikniętego pola zapisane jest w postaci: LOCAL_BOARD_ID * 10 + ID_OF_FIELD_IN_LOCAL_BOARD.
    # Przykład:
    # - dla prawego górnego pola środkowej górnej planszy ID = '12',
    # - dla środkowego pola środkowej planszy ID = '44'
    id = int(data['id'])
    board = id // 10
    field = id % 10
    # Jeżeli ruch jest możliwy
    if game.makeMove(board, field):
        # Jeśli po wykonaniu ruchu plansza przestaje być grywalna, usuwamy ją z listy
        # grywalnych plansz w obiekcie game
        if game.isBoardNotPlayable(board):
            game.playableFields.remove(board)

        nextBoard = game.getNextBoard()

        if nextBoard == 9:
            toLighten = game.playableFields
        else:
            toLighten.append(nextBoard)

        viewData['symbol'] = game.whoseTurnSymbol
        viewData['toLighten'] = toLighten
        viewData['localGameEnded'] = False
        viewData['localBoardWinner'] = ''
        viewData['globalGameEnded'] = False
        viewData['globalBoardWinner'] = ''
        # Na planszy zakończyła się rozgrywka (wygrana jednego z graczy na danej
        # planszy lokalnej lub remis na tej planszy)
        if game.isBoardNotPlayable(board):
            # Wygranana na planszy lokalnej jednego z graczy
            if game.playerSymbol[game.checkLocalWin()] != "none":
                viewData['localGameEnded'] = True
                viewData['localBoardWinner'] = game.whoseTurnSymbol
            # Sprawdzenie czy zakończyła się rozgrywka (remis lub wygrana jednego z graczy)
            if game.checkGameEnded():
                # Wygrana gry przez jednego z graczy
                if game.playerSymbol[game.checkGlobalWin()] != "none":
                    viewData['globalGameEnded'] = True
                    viewData['globalBoardWinner'] = viewData['localBoardWinner']
                    game.scoreTable[game.whoseTurnSymbol] += 1
                # remis
                else:
                    viewData['localGameEnded'] = True
                    viewData['globalGameEnded'] = True
                    game.scoreTable['X'] += 1
                    game.scoreTable['O'] += 1
                # przygotowanie nowej rundy
                game.prepareNewRound()
        for sid in room.clients:
            fsio.emit('actualizeView', viewData, room=sid)

## Obsługuje żądanie wysłania wiadomości do czatu przez klienta
#  Wysyła zdarzenia aktualizujące stan czatu u każdego z klientów przebywających w pokoju,
#  w którym przebywa gracz wysyłający żądanie
#  @param data - słownik, w kórym klient przesyła treść wiadomości
#  @param socketId - id socketu, z którego zostało wysłane żądanie dołączenia do pokoju
def handleReceivedMessage(data, socketId):
    receivedMessageData = {
        'msg': data['msg']
    }
    room = getRoomClientIsConnectedTo(socketId)
    receivedMessageData['who'] = 'self'
    fsio.emit('receivedMessage', receivedMessageData, room=socketId)
    receivedMessageData['who'] = 'friend'
    for sid in room.clients:
        fsio.emit('receivedMessage', receivedMessageData, room=sid, include_self=False)

## Obsługuje żądanie dołączenia do pokoju przez klienta
#  Zwraca parę gameActivated, room:<br>
#  gameActivated - True jeśli gra została aktywowana po opuszczeniu pokoju przez gracza, False - w p.p.(bool)<br>
#  room - obiekt klasy room, do którego dołączył klient (None jeśli klient podał nieprawidłowe ID pokoju)
#  @param data - słownik, w kórym klient przesyła id pokoju, do którego choice dołączyć
#  @param socketId - id socketu, z którego zostało wysłane żądanie dołączenia do pokoju
def handleJoinRoom(data, socketId):
    room = getRoomById(data['roomId'])
    joinData = {'roomId': data['roomId']}
    gameActivated = False
    if room is not None:
        joinData['advancedMode'] = room.advancedMode
        joinData['playTime'] = room.playTime
        fsio.emit('joinRoom', joinData, room=socketId)
        room.connectClient(socketId)
        # Jeżeli po dołączeniu klienta jest conajmnie dwóch graczy i ...
        if len(room.whoseSocket) >= 2:
            # ... gra nie była aktywna - start gry dla wszystkich graczy w pokoju
            if not room.isGameActive:
                gameActivated = True
                for sid in room.clients:
                    fsio.emit('startGame', room=sid)
                room.isGameActive = True
            # ... gra była aktywna - start gry tylko dla gracza, który dołączył
            else:
                fsio.emit('startGame', room=socketId)
    return gameActivated, room

## Obsługuje żądanie opuszczenia pokoju przez klienta
#  Zwraca parę gameActivated, room:<br>
#  gameActivated - True jeśli gra została aktywowana po opuszczeniu pokoju przez gracza, False - w p.p.(bool)<br>
#  room - obiekt klasy room, który został opuszczony przez klienta (None jeśli klient nie był w żadnym pokoju)
#  @param socketId - id socketu, z którego zostało wysłane żądanie opuszczenia pokoju
def handleLeaveRoom(socketId):
    gameActivated = False
    room = getRoomClientIsConnectedTo(socketId)
    if room is not None:
        # Jeżeli użytkownik uczestniczył w rozgrywce - stop gry
        if room.disconnectClient(socketId):
            for sid in room.clients:
                fsio.emit('stopGame', room=sid)
            # Jeżeli jest conajmniej dwóch graczy w pokoju - rozpocznij nową grę
            if room.numberOfConnectedClients >= 2:
                gameActivated = True
                room.isGameActive = True
                for sid in room.clients:
                    fsio.emit('startGame', room=sid)
    # Stop gry dla danego gracza oraz opuszczenie pokoju
    fsio.emit('stopGame', room=socketId)
    fsio.emit('leaveRoom', room=socketId)
    return gameActivated, room

## Obsługuje połączenie klienta z serwerem
#  Aktualizuje widok dostępnych pokojów u klienta, który właśnie połączył się z serwerem
#  @param socketId - id socketu klienta, który uzyskał połączenie z serwerem.
def handleConnection(socketId):
    roomsData = []
    for el in rooms:
        room = el['room']
        mode = 'casual'
        playTime = '-'
        if room.advancedMode:
            mode = 'advanced'
            playTime = str(room.playTime) + ' s'
        roomsData.append(
            {'roomName': room.name,
             'mode': mode,
             'playTime': playTime,
             'roomId': room.id
             }
        )
    fsio.emit('initializeRoomsList', roomsData, room=socketId)

## Obsługuje rozłączenie użytkownika z serwerem
#  @param socketId - id socketu klienta, który rozłącza się z serwerem.
def handleDisconnection(socketId):
    handleLeaveRoom(socketId)
    fsio.emit('disconnect', room=socketId)
