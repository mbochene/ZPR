from engine import *


class Game:
    def __init__(self):
        self.prepareNewRound()
        self.playerSymbol = {
            PlayerSymbol.none: "none",
            PlayerSymbol.X: 'X',
            PlayerSymbol.O: 'O'
        }
        self.scoreTable = {
            'X': 0,
            'O': 0
        }

    def prepareNewRound(self):
        self.gameState = GameState()
        self.playableFields = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def prepareNewGame(self):
        self.prepareNewRound()
        self.scoreTable['X'] = 0
        self.scoreTable['O'] = 0

    def makeMove(self, board, field):
        self.whoseTurnSymbol = self.playerSymbol[self.getWhoseTurn()]
        return self.gameState.makeMove(board, field)

    def checkLocalWin(self):
        return self.gameState.checkLocalWin()

    def checkGlobalWin(self):
        return self.gameState.checkGlobalWin()

    def getWhoseTurn(self):
        return self.gameState.getWhoseTurn()

    def isBoardNotPlayable(self, board):
        return self.gameState.isBoardNotPlayable(board)

    def getNextBoard(self):
        return self.gameState.getNextBoard()
