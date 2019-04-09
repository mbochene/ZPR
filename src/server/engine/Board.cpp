#include "headers/Board.hpp"
#include <iostream>
Board::Board() : emptyFields(9), end(false), winner(PlayerSymbol::NONE)
{
    for(int i=0;i<9;i++)
        fields[i]=PlayerSymbol::NONE;
}

Board::~Board(){}

Board::PlayerSymbol Board::isWin()
{
    for(int i=0;i<3;i++)
    {
        if(fields[i*3]==fields[i*3+1] && fields[i*3+1]==fields[i*3+2])      // sprawdzanie czy wygrana w poziomie
        {
            if(fields[i*3]!=PlayerSymbol::NONE)
                return fields[i*3];
        }
        if(fields[i]==fields[i+3] && fields[i+3]==fields[i+6])              // sprawdzanie czy wygrana w pionie
        {
            if(fields[i]!=PlayerSymbol::NONE)
                return fields[i];
        }
    }

    if(fields[0]==fields[4] && fields[4]==fields[8])                // sprawdzanie czy wygrana w skosie
    {
        if(fields[0]!=PlayerSymbol::NONE)
            return fields[0];
    }

    if(fields[2]==fields[4] && fields[4]==fields[6])                // sprawdzanie czy wygrana w skosie
    {
        if(fields[2]!=PlayerSymbol::NONE)
            return fields[2];
    }

    return PlayerSymbol::NONE;
}

bool Board::isPickPossible(const int &field)
{
    if(fields[field]!=PlayerSymbol::NONE)
        return false;

    return true;
}

bool Board::pickField(const int &field, const Board::PlayerSymbol &player)
{
    if(!isPickPossible(field))
        return false;

    emptyFields--;
    fields[field]=static_cast<PlayerSymbol>(player);

    PlayerSymbol i=isWin();

    if(emptyFields==0 || i!=PlayerSymbol::NONE)
    {
        end=true;
        winner=i;
    }

    return true;
}

bool Board::gameEnded()
{
    return end;
}

Board::PlayerSymbol Board::getWinner()
{
    return winner;
}
