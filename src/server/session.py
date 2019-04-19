from game import Game

class Session:
    def __init__(self):
        self.numberOfConnectedClients = 0
        self.clients = []
        self.whoseSocket = {}
        self.game = Game()
        self.isGameActive = False

    def connectClient(self, socketId):
        self.numberOfConnectedClients += 1
        dictLength = len(self.whoseSocket)
        print ("dict length: %d" % (dictLength))
        if dictLength < 2:
            self.whoseSocket[socketId] = dictLength + 1
        for i in self.whoseSocket:
            print ("%s : %d" % (i, self.whoseSocket[i]))
        print ("dict length after: %d" % (len(self.whoseSocket)))

    def disconnectClient(self, socketId):               # zwraca true jesli odlacza sie jeden z grajacych; w.p.p. zwraca false
        self.numberOfConnectedClients -= 1
        if self.whoseSocket.get(socketId) != None:
            self.isGameActive = False
            self.game.prepareNewGame()
            self.whoseSocket.pop(socketId)
            for socket in self.whoseSocket:             # jak 1 gracz sie odlaczy, to 2 gracz ma stac sie 1 graczem
                self.whoseSocket[socket] = 1            # dodac emita restartujacego gre
            return True
        return False
            
    def getNumberOfConnectedClients(self):
        return self.numberOfConnectedClients