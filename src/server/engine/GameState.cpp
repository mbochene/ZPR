#include "headers/GameState.hpp"
#include "headers/Board.hpp"
#include <iostream>

/** \file GameState.cpp
*   \brief Plik zawierający definicje metod klasy "GameState".
*/


GameState::GameState() : whoseTurn(Board::PlayerSymbol::X), lastChosenBoard(0), nextBoard(9)
{
    for(int i=0; i<9; i++)
        localBoards.push_back(PBoard(new Board));
    globalBoard= PBoard(new Board);
}

GameState::~GameState(){}

bool GameState::makeMove(const int &board, const int &field)
{
    bool isBoardIncorrect = (nextBoard!=9 && board!=nextBoard) || !globalBoard->isPickPossible(board) || localBoards[board]->gameEnded();  // plansza jest niepoprawnie wybrana, gdy gracz spróbuje wybrać inną planszę niż wynika to z poprzedniego ruchu lub (w przypadku gdy może grać na każdej) planszę, na której gra się skończyła

    if(isBoardIncorrect || !localBoards[board]->pickField(field, whoseTurn))
        return false;
    
    whoseTurn=static_cast<Board::PlayerSymbol>(static_cast<int>(whoseTurn)%2+1);
    lastChosenBoard=board;
    lastChosenField=field;

    if(localBoards[lastChosenField]->gameEnded())                                // jeśli na następnej planszy nie można zagrać, to można grać na każdej
        nextBoard=9;
    else
        nextBoard=lastChosenField;

    return true;
}

Board::PlayerSymbol GameState::checkLocalWin()
{
    Board::PlayerSymbol i=localBoards[lastChosenBoard]->getWinner();
    if(i!=Board::PlayerSymbol::NONE)
    {
        globalBoard->pickField(lastChosenBoard,static_cast<Board::PlayerSymbol>(static_cast<int>(whoseTurn)%2+1));
        return i;
    }
    return Board::PlayerSymbol::NONE;
}

Board::PlayerSymbol GameState::checkGlobalWin()
{
    return globalBoard->getWinner();
}

Board::PlayerSymbol GameState::getWhoseTurn()
{
    return whoseTurn;
}

bool GameState::isBoardNotPlayable(const int &board)
{
    return localBoards[board]->gameEnded();
}

int GameState::getNextBoard()
{
    return nextBoard;
}

bool GameState::gameEnded()
{
    return globalBoard->gameEnded();
}