CC = g++
CPPFLAGS = -lboost_unit_test_framework -Wall -Wextra -pedantic -std=c++11
PYLIBPATH = $(shell python-config --exec-prefix)/lib
LIB = -L$(PYLIBPATH) $(shell python-config --libs) -lboost_python
OPTS = $(shell python-config --includes) -O2

all: test engine.so
	./test --log_level=test_suite

test:
	$(CC) -o test headers/GameState.hpp headers/Board.hpp Board.cpp GameState.cpp tests/tests.cpp $(CPPFLAGS)

GameState.o: GameState.cpp headers/GameState.hpp
	$(CC) $(OPTS) -c -fPIC GameState.cpp -o GameState.o

Board.o: Board.cpp headers/Board.hpp
	$(CC) $(OPTS) -c -fPIC Board.cpp -o Board.o

engine.so: GameState.o Board.o
	$(CC) $(LIB) -shared -o ../engine.so GameState.o Board.o $(CPPFLAGS)

clean:
	rm -rf ../engine.so *.o test
