#!venv/bin/python3

## \file game.py
#   Plik zawierający definicję klasy "Game".
import engine as en

## Klasa reprezentująca pojedynczą grę (mogącą składać się z wielu rund).
class Game:
    ## Konstruktor. Tworzy nową grę, ustawia słowniki reprezentujące symbole graczy oraz tablicę wyników.
    # @param self
    def __init__(self):
        self.prepareNewRound()
        self.playerSymbol = {
            en.PlayerSymbol.none: "none",
            en.PlayerSymbol.X: 'X',
            en.PlayerSymbol.O: 'O'
        }
        self.scoreTable = {
            'X': 0,
            'O': 0
        }

    ## Przygotowuje nową rundę gry.
    # @param self
    def prepareNewRound(self):
        self.gameState = en.GameState()
        self.playableFields = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Przygotowuje nową grę (nowa runda oraz wyzerowanie tablicy wyników).
    # @param self
    def prepareNewGame(self):
        self.prepareNewRound()
        self.scoreTable['X'] = 0
        self.scoreTable['O'] = 0

    ## Woła metodę silnika "makeMove".
    # @param self
    # @param board  Numer planszy.
    # @param field  Numer pola na wybranej planszy.
    def makeMove(self, board, field):
        self.whoseTurnSymbol = self.playerSymbol[self.getWhoseTurn()]
        return self.gameState.makeMove(board, field)

    ## Woła metodę silnika "checkLocalWin".
    # @param self
    def checkLocalWin(self):
        return self.gameState.checkLocalWin()

    ## Woła metodę silnika "checkGlobalWin".
    # @param self
    def checkGlobalWin(self):
        return self.gameState.checkGlobalWin()

    ## Woła metodę silnika "getWhoseTurn".
    # @param self
    def getWhoseTurn(self):
        return self.gameState.getWhoseTurn()

    ## Woła metodę silnika "isBoardNotPlayable".
    # @param self
    # @param board  Numer sprawdzanej planszy.
    def isBoardNotPlayable(self, board):
        return self.gameState.isBoardNotPlayable(board)

    ## Woła metodę silnika "getNextBoard".
    # @param self
    def getNextBoard(self):
        return self.gameState.getNextBoard()
