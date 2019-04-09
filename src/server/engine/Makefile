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
	$(CC) $(OPTS) -c -fPIC GameState.cpp -o GameState.o $(CPPFLAGS)

Board.o: Board.cpp headers/Board.hpp
	$(CC) $(OPTS) -c -fPIC Board.cpp -o Board.o $(CPPFLAGS)

module.o:
	$(CC) $(OPTS) -c -fPIC module.cpp -o module.o $(CPPFLAGS)

engine.so: GameState.o Board.o module.o
	$(CC) -shared -Wl,-soname,../engine.so -o ../engine.so GameState.o Board.o module.o $(LIB) $(CPPFLAGS)

clean:
	rm -rf ../engine.so *.o test
