#include "headers/GameState.hpp"
#include "headers/Board.hpp"
#include <iostream>
GameState::GameState()
{
    whoseTurn=1;
    nextBoard=9;
    lastChosenBoard=0;
}

GameState::~GameState(){};

////////////// czy zakładać błędy api ??? ///////////

bool GameState::makeMove(const int &board, const int &field, const int &player)
{
    bool isBoardIncorrect = (nextBoard!=9 && board!=nextBoard) || !globalBoard.isPickPossible(board) || localBoards[board].gameEnded();  // plansza jest niepoprawnie wybrana, gdy gracz spróbuje wybrać inną planszę niż wynika to z poprzedniego ruchu lub (w przypadku gdy może grać na każdej) planszę, na której gra się skończyła

    if(isBoardIncorrect || !localBoards[board].pickField(field, player))
        return false;
    
    whoseTurn=whoseTurn%2+1;
    lastChosenBoard=board;
    lastChosenField=field;

    if(localBoards[lastChosenField].gameEnded())                                // jeśli na następnej planszy nie można zagrać, to można grać na każdej
        nextBoard=9;
    else
        nextBoard=lastChosenField;

    return true;
}

int GameState::checkLocalWin()
{
    int i=localBoards[lastChosenBoard].getWinner();
    if(i!=0)
    {
        globalBoard.pickField(lastChosenBoard,whoseTurn%2+1);
        return i;
    }
    return 0;
}

int GameState::checkGlobalWin()
{
    return globalBoard.getWinner();
}

// cos do ustawiania next board