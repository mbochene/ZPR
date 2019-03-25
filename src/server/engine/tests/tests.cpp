#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE EngineTests
#include "../headers/Board.hpp"
#include "../headers/GameState.hpp"
#include <boost/test/unit_test.hpp>
#include <boost/test/test_tools.hpp>

using move_pair = std::pair<int, int>;

void pickFields(Board &x, std::initializer_list<move_pair> moves)
{
    for(const move_pair &move : moves)
    {
        x.pickField(move.first, move.second);
    }
}

BOOST_AUTO_TEST_SUITE(BoardTests)

BOOST_AUTO_TEST_CASE(testPickEmptyField)
{
    Board x;
    BOOST_CHECK_EQUAL(x.pickField(0,1), true);
}

BOOST_AUTO_TEST_CASE(testCheckFieldLock)
{
    Board x;
    x.pickField(0,1);
    BOOST_CHECK_EQUAL(x.pickField(0,2), false);
}

BOOST_AUTO_TEST_CASE(testHorizontalWin1)
{
    Board x;
    pickFields(x,{{0,1}, {1,1}, {2,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testHorizontalWin2)
{
    Board x;
    pickFields(x,{{3,1}, {4,1}, {5,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testHorizontalWin3)
{
    Board x;
    pickFields(x,{{6,1}, {7,1}, {8,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testVerticalWin1)
{
    Board x;
    pickFields(x,{{0,1}, {3,1}, {6,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testVerticalWin2)
{
    Board x;
    pickFields(x,{{1,1}, {4,1}, {7,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testVerticalWin3)
{
    Board x;
    pickFields(x,{{2,1}, {5,1}, {8,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testDiagonalWin1)
{
    Board x;
    pickFields(x,{{0,1}, {4,1}, {8,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testDiagonalWin2)
{
    Board x;
    pickFields(x,{{2,1}, {4,1}, {6,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 1);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testDraw)
{
    Board x;
    pickFields(x,{{4,1}, {2,2}, {8,1}, {0,2}, {1,1}, {7,2}, {3,1}, {5,2}, {6,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 0);
    BOOST_CHECK_EQUAL(x.gameEnded(), true);
}

BOOST_AUTO_TEST_CASE(testIngameSituation1)
{
    Board x;
    pickFields(x,{{0,1}, {1,2}, {2,1}});
    BOOST_CHECK_EQUAL(x.getWinner(), 0);
    BOOST_CHECK_EQUAL(x.gameEnded(), false);
}

BOOST_AUTO_TEST_SUITE_END()

BOOST_AUTO_TEST_SUITE(GameStateTests)

BOOST_AUTO_TEST_CASE(testMakeProperMove1)
{
    GameState x;
    BOOST_CHECK_EQUAL(x.getWhoseTurn(), 1);
    BOOST_CHECK_EQUAL(x.makeMove(0,0), true);
    BOOST_CHECK_EQUAL(x.getWhoseTurn(), 2);
}

BOOST_AUTO_TEST_CASE(testNextBoardChoice1)
{
    GameState x;
    x.makeMove(0,1);
    BOOST_CHECK_EQUAL(x.makeMove(1,0), true);
    BOOST_CHECK_EQUAL(x.makeMove(3,1), false);
    BOOST_CHECK_EQUAL(x.makeMove(0,0), true);
}

BOOST_AUTO_TEST_CASE(testCheckLocalAndGlobalWin)
{
    GameState x;
    x.makeMove(0,1);
    BOOST_CHECK_EQUAL(x.checkLocalWin(), 0);
    x.makeMove(1,0);
    x.makeMove(0,2);
    x.makeMove(2,0);
    x.makeMove(0,0);
    BOOST_CHECK_EQUAL(x.checkLocalWin(), 1);
    BOOST_CHECK_EQUAL(x.checkGlobalWin(), 0);
    BOOST_CHECK_EQUAL(x.makeMove(0,5), false);          //sprawdzenie czy można ruszyć się na planszy, na której wygrał jeden z graczy
    x.makeMove(5,3);
    x.makeMove(3,6);
    x.makeMove(6,3);
    x.makeMove(3,0);
    x.makeMove(7,3);
    x.makeMove(3,3);
    BOOST_CHECK_EQUAL(x.checkLocalWin(), 1);
    BOOST_CHECK_EQUAL(x.checkGlobalWin(), 0);
    x.makeMove(8,6);
    x.makeMove(6,7);
    x.makeMove(7,6);
    x.makeMove(6,8);
    x.makeMove(8,3);
    x.makeMove(6,6);
    BOOST_CHECK_EQUAL(x.checkLocalWin(), 1);
    BOOST_CHECK_EQUAL(x.checkGlobalWin(), 1);
}

BOOST_AUTO_TEST_SUITE_END()