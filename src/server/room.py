#!venv/bin/python3
## \file room.py
# Plik zawierający definicję klasy "Room"
import game
import time

## Klasa reprezentująca pokój - jest to obiekt dzielący użytkowników na grupy
#  i pozwalający na rozgrywanie wielu gier jednocześnie.
class Room:
    ## Konstruktor. Tworzy nowy pokój. Wywołuje konstruktor klasy game.Game i przypisuje
    #  stworzony obiekt jako własny, unikalny atrybut przechowujący informacje o stanie
    #  gry w danym pokoju. Ustawia niezbędne dane pokoju, inicjuje listę klientów
    #  przebywających w pokoju oraz słownik przechowujacy informacje o tym,
    #  którzy klienci aktualnie toczą rozgrywkę (pary socketId -> symbol).
    #  @param self
    #  @param socketId - id socketu użytkownika, który wysłał żądanie utworzenia pokoju (string)
    #  @param roomId - wygenerowane losowo unikalne id tworzonego pokoju (string)
    #  @param roomName - nazwa tworzonego pokoju (string)
    #  @param advancedMode - decyduje o tym czy gra w danym pokoju będzie toczyć się
    #                        z ograniczeniem czasowym (bool) : parametr opcjonalny
    #  @param playTime - maksymalny czas przeznaczony na grę dla jednego gracza (int):
    #                    parametr opcjonalny
    def __init__(self, socketId, roomId, roomName, advancedMode=False, playTime=0):
        ## id socketu właściciela pokoju
        self.hostSocketId = socketId
        ## id pokoju
        self.id = roomId
        ## nazwa pokoju
        self.name = roomName
        ## atrybut informujący o trybie rozgrywki (True - advanced, "na czas"; False - zwykła rozgrywka)
        self.advancedMode = advancedMode
        ## czas rozgrywki (atrybut nieistotny gdy advanedMode == False)
        self.playTime = playTime
        ## atrybut przechowujący liczbę użytkowników przebywających w pokoju
        self.numberOfConnectedClients = 0
        ## lista użytkowników przebywających w pokoju
        self.clients = []
        ## słownik przechowujący informację o tym kto aktualnie toczy rozgrywkę
        self.whoseSocket = {}
        ## obiekty klasy game.Game - unikalny obiekt dla danego pokoju przechowujący
        #  aktualny stan gry.
        self.game = game.Game()
        ## atrybut przechowujący informację o tym, czy gra jest aktywna (True - aktywna; False - nieaktywna)
        self.isGameActive = False
    ## Dołącza użytkownika do pokoju. Jeśli aktualnie w pokoju przebywa mniej
    #  niż dwóch użytkowników, dołączający do pokoju użytkownik zapisywany jest w słowniku
    #  przechowującym informacje o tym, którzy klienci aktualnie toczą rozgrywkę.
    #  @pararm self
    #  @param socketId - id socketu użytkownika, który wysłał żądanie o dołączenie do pokoju
    def connectClient(self, socketId):
        self.numberOfConnectedClients += 1
        self.clients.append(socketId)
        dictLength = len(self.whoseSocket)
        if dictLength < 2:
            self.whoseSocket[socketId] = dictLength + 1

    ## Usuwa użytkownika z pokoju. Jeśli użytkownik znajdował się w słowniku
    #  przechowującym informacje o tym, kto aktualnie toczy rozgrywkę i do pokoju
    #  połączonych było więcej niż dwóch użytkowników, do słownika, na miejsce
    #  użytkownika opuszczajacego pokój dopisywany jest pierwszy użytkownik z listy
    #  połączonych z pokojem nie znajdujący się w słowniku.<br>
    #  Zwraca:<br>
    #  True - w przypadku gdy pokój opuszcza jeden z grających użytkowników<br>
    #  False - w przeciwnym przypadku
    #  @param self
    #  @param socketId - id socketu użytkownika, który wysłał żądanie o opuszczenie pokoju.
    def disconnectClient(self, socketId):
        self.numberOfConnectedClients -= 1
        self.clients.remove(socketId)
        if self.whoseSocket.get(socketId) != None:
            self.isGameActive = False
            self.game.prepareNewGame()
            self.whoseSocket.pop(socketId)
            for socket in self.whoseSocket:             # jak 1 gracz sie odlaczy, to 2 gracz ma stac sie 1 graczem
                # dodac emita restartujacego gre
                self.whoseSocket[socket] = 1
            if self.numberOfConnectedClients >= 2:
                self.whoseSocket[self.clients[1]] = 2
            return True
        return False
    ## Sprawdza czy dany użytkownik znajduje się na liście użytkowników przebywających
    #  w pokoju<br>
    #  Zwraca:<br>
    #  True - w przypadku gdy użytkownik znajduje sie na liście<br>
    #  False - w przeciwnym przypadku
    #  @param self
    #  @param socketId - id socketu użytkownika, którego należy wyszukać na liście użytkowników
    #                    przebywających w pokoju
    def isClientConnected(self, socketId):
        return socketId in self.clients
