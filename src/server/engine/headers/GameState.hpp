#ifndef GAME_STATE_HPP
#define GAME_STATE_HPP
#include "Board.hpp"
#include <memory>
#include <vector>

typedef std::shared_ptr<Board> PBoard;                      // nie unique, bo boost python ma problem

class GameState
{
    Board::PlayerSymbol whoseTurn;                  // czyja tura (przyjmuje wartość 1 lub 2)
    int lastChosenBoard;            // numer planszy, na której odbył się ostatni prawidłowy ruch
    int lastChosenField;            // ostatnie prawidłowo wybrane pole
    int nextBoard;                  // numer planszy, na której ma być wykonany następny ruch; jeśli z przedziału [0;8], to na 1 z 9 plansz; jeśli 9, to na każdej planszy (jeśli nie wygrana/remis)
    std::vector<PBoard> localBoards;              // wektor 9 lokalnych plansz
    PBoard globalBoard;              // globlana plansza

    public:
    GameState();
    ~GameState();

    bool makeMove(const int &board, const int &field); // metoda pozwalająca na "postawienie" kółka lub krzyżyka na danej planszy; zwraca true i zmienia wartości zmiennych lokalnych, jeśli operacja się powiedzie
    Board::PlayerSymbol checkLocalWin();   //metoda sprawdzająca czy ostatni ruch doprowadził do wygranej na planszy lokalnej; zwraca numer gracza jeśli tak; w.p.p zwraca 0
    Board::PlayerSymbol checkGlobalWin();  // metoda sprawdzająca czy ostatni ruch doprowadził do wygranej na planszy globlanej; zwraca numer gracza jeśli tak; w.p.p zwraca 0
    Board::PlayerSymbol getWhoseTurn();    // metoda zwracająca numer gracza, który ma ruch
    bool isBoardNotPlayable(const int &board); // metoda zwracająca informację czy na danej planszy można wykonać ruch
    int getNextBoard();    // zwraca wartość zmiennej nextBoard
};

#endif

