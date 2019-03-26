CC = g++
CPPFLAGS = -lboost_unit_test_framework -Wall -Wextra -pedantic -std=c++11
PYLIBPATH = $(shell python-config --exec-prefix)/lib
LIB = -L$(PYLIBPATH) $(shell python-config --libs) -lboost_python
OPTS = $(shell python-config --includes) -O2

all: test module
	./test --log_level=test_suite

test:
	$(CC) -o test headers/GameState.hpp headers/Board.hpp Board.cpp GameState.cpp tests/tests.cpp $(CPPFLAGS)

module:
	$(CC) $(OPTS) $(LIB) -shared -fPIC -o ../engine.so headers/GameState.hpp headers/Board.hpp Board.cpp GameState.cpp module.cpp $(CPPFLAGS)

clean:
	rm -rf ../engine.so test