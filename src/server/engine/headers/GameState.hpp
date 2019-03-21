#include <vector>
#include "Board.hpp"
#ifndef GAME_STATE_HPP
#define GAME_STATE_HPP

class GameState
{
    int whoseTurn;
    std::vector<Board> localBoards;
    Board globalBoard;
};

#endif