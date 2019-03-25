#include "headers/Board.hpp"
#include <iostream>
Board::Board()
{
    for(int i=0;i<9;i++)
        fields[i]=0;

    emptyFields=9;
    end=false;
    winner=0;
}

Board::~Board(){}

////////////// czy zakładać błędy api ??? ///////////

int Board::isWin()
{
    for(int i=0;i<3;i++)
    {
        if(fields[i*3]==fields[i*3+1] && fields[i*3+1]==fields[i*3+2])      // sprawdzanie czy wygrana w poziomie
        {
            if(fields[i*3]!=0)
                return fields[i*3];
        }
        if(fields[i]==fields[i+3] && fields[i+3]==fields[i+6])              // sprawdzanie czy wygrana w pionie
        {
            if(fields[i]!=0)
                return fields[i];
        }
    }

    if(fields[0]==fields[4] && fields[4]==fields[8])                // sprawdzanie czy wygrana w skosie
    {
        if(fields[0]!=0)
            return fields[0];
    }

    if(fields[2]==fields[4] && fields[4]==fields[6])                // sprawdzanie czy wygrana w skosie
    {
        if(fields[2]!=0)
            return fields[2];
    }

    return 0;
}

bool Board::isPickPossible(const int &field)
{
    if(fields[field]!=0)
        return false;

    return true;
}

bool Board::pickField(const int &field, const int &player)
{
    if(!isPickPossible(field))
        return false;

    emptyFields--;
    fields[field]=player;

    int i=isWin();

    if(emptyFields==0 || i!=0)
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

int Board::getWinner()
{
    return winner;
}
