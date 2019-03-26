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
    ;
}