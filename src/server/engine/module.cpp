#include "headers/GameState.hpp"
#include <boost/python.hpp>

BOOST_PYTHON_MODULE(engine)
{
    using namespace boost::python;

    class_<GameState>("GameState")
        .def("makeMove", &GameState::makeMove)
        .def("checkLocalWin", &GameState::checkLocalWin)
        .def("checkGlobalWin", &GameState::checkGlobalWin)
        .def("getWhoseTurn", &GameState::getWhoseTurn)
        .def("isBoardNotPlayable", &GameState::isBoardNotPlayable)
        .def("getNextBoard", &GameState::getNextBoard);

    enum_<Board::PlayerSymbol>("PlayerSymbol")
        .value("none", Board::PlayerSymbol::NONE)
        .value("X", Board::PlayerSymbol::X)
        .value("O", Board::PlayerSymbol::O)
    ;
}