#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE EngineTests
#include "../headers/Board.hpp"
#include "../headers/GameState.hpp"
#include <boost/test/unit_test.hpp>
#include <boost/test/test_tools.hpp>

using pick_pair = std::pair<int, Board::PlayerSymbol>;
using move_pair = std::pair<int, int>;

/** \file tests.cpp
*   \brief Plik zawierający testy jednostkowe silnika gry.
*/

void pickFields(Board &x, std::initializer_list<pick_pair> picks)
{
    for (const pick_pair &pick : picks)
    {
        x.pickField(pick.first, pick.second);
    }
}

void makeMoves(GameState &x, std::initializer_list<move_pair> moves)
{
    for (const move_pair &move : moves)
    {
        x.makeMove(move.first, move.second);
    }
}

BOOST_AUTO_TEST_SUITE(BoardTests)

BOOST_AUTO_TEST_CASE(testPickEmptyField)
{
    Board x;
    BOOST_CHECK_EQUAL(x.pickField(0, Board::PlayerSymbol::X), true);
}

BOOST_AUTO_TEST_CASE(testCheckFieldLock)
{
    Board x;
    x.pickField(0, Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.pickField(0, Board::PlayerSymbol::O), false);
}

BOOST_AUTO_TEST_CASE(testHorizontalWin1)
{
    Board x;
    pickFields(x, {{0, Board::PlayerSymbol::X}, {1, Board::PlayerSymbol::X}, {2, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testHorizontalWin2)
{
    Board x;
    pickFields(x, {{3, Board::PlayerSymbol::X}, {4, Board::PlayerSymbol::X}, {5, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testHorizontalWin3)
{
    Board x;
    pickFields(x, {{6, Board::PlayerSymbol::X}, {7, Board::PlayerSymbol::X}, {8, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testVerticalWin1)
{
    Board x;
    pickFields(x, {{0, Board::PlayerSymbol::X}, {3, Board::PlayerSymbol::X}, {6, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testVerticalWin2)
{
    Board x;
    pickFields(x, {{1, Board::PlayerSymbol::X}, {4, Board::PlayerSymbol::X}, {7, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testVerticalWin3)
{
    Board x;
    pickFields(x, {{2, Board::PlayerSymbol::X}, {5, Board::PlayerSymbol::X}, {8, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testDiagonalWin1)
{
    Board x;
    pickFields(x, {{0, Board::PlayerSymbol::X}, {4, Board::PlayerSymbol::X}, {8, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testDiagonalWin2)
{
    Board x;
    pickFields(x, {{2, Board::PlayerSymbol::X}, {4, Board::PlayerSymbol::X}, {6, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testDraw)
{
    Board x;
    pickFields(x, {{4, Board::PlayerSymbol::X}, {2, Board::PlayerSymbol::O}, {8, Board::PlayerSymbol::X}, {0, Board::PlayerSymbol::O}, {1, Board::PlayerSymbol::X}, {7, Board::PlayerSymbol::O}, {3, Board::PlayerSymbol::X}, {5, Board::PlayerSymbol::O}, {6, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::NONE);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testIngameSituation1)
{
    Board x;
    pickFields(x, {{0, Board::PlayerSymbol::X}, {1, Board::PlayerSymbol::O}, {2, Board::PlayerSymbol::X}});
    BOOST_CHECK_EQUAL(x.getWinner(), Board::PlayerSymbol::NONE);
    BOOST_CHECK_EQUAL(x.gameEnded(), false);
}

BOOST_AUTO_TEST_SUITE_END()

BOOST_AUTO_TEST_SUITE(GameStateTests)

BOOST_AUTO_TEST_CASE(testMakeProperMove1)
{
    GameState x;
    BOOST_CHECK_EQUAL(x.getWhoseTurn(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.makeMove(0, 0), true);
    BOOST_CHECK_EQUAL(x.getWhoseTurn(), Board::PlayerSymbol::O);
}

BOOST_AUTO_TEST_CASE(testNextBoardChoice1)
{
    GameState x;
    x.makeMove(0, 1);
    BOOST_CHECK_EQUAL(x.makeMove(1, 0), true);
    BOOST_CHECK_EQUAL(x.makeMove(3, 1), false);
    BOOST_CHECK_EQUAL(x.makeMove(0, 0), true);
}

BOOST_AUTO_TEST_CASE(testCheckLocalAndGlobalWin)
{
    GameState x;
    x.makeMove(0, 1);

    BOOST_CHECK_EQUAL(x.checkLocalWin(), Board::PlayerSymbol::NONE);

    makeMoves(x, {{1, 0}, {0, 2}, {2, 0}, {0, 0}});

    BOOST_CHECK_EQUAL(x.checkLocalWin(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.checkGlobalWin(), Board::PlayerSymbol::NONE);
    BOOST_CHECK_EQUAL(x.makeMove(0, 5), false); //sprawdzenie czy można ruszyć się na planszy, na której wygrał jeden z graczy

    makeMoves(x, {{5, 3}, {3, 6}, {6, 3}, {3, 0}, {7, 3}, {3, 3}});

    BOOST_CHECK_EQUAL(x.checkLocalWin(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.checkGlobalWin(), Board::PlayerSymbol::NONE);

    makeMoves(x, {{8, 6}, {6, 7}, {7, 6}, {6, 8}, {8, 3}, {6, 6}});

    BOOST_CHECK_EQUAL(x.checkLocalWin(), Board::PlayerSymbol::X);
    BOOST_CHECK_EQUAL(x.checkGlobalWin(), Board::PlayerSymbol::X);
}

BOOST_AUTO_TEST_SUITE_END()
