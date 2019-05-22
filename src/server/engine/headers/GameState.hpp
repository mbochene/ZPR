#ifndef GAME_STATE_HPP
#define GAME_STATE_HPP
#include "Board.hpp"
#include <memory>
#include <vector>

typedef std::shared_ptr<Board> PBoard;

/** \file GameState.hpp
*   \brief Plik nagłówkowy zawierający definicję klasy "GameState".
*/


/*! \brief Klasa reprezentująca pojedyńczą rozgrywkę.
*
*   W jej skład wchodzi 9 plansz mikro, plansza makro oraz zmienne pozwalające na rozstrzygnięcie stanu rozgrywki.
*/
class GameState
{
    Board::PlayerSymbol whoseTurn;                  // czyja tura (przyjmuje wartość X lub O)
    int lastChosenBoard;                            // numer planszy, na której odbył się ostatni prawidłowy ruch
    int lastChosenField;                            // ostatnie prawidłowo wybrane pole
    int nextBoard;                                  // numer planszy, na której ma być wykonany następny ruch; jeśli z przedziału [0;8], to na 1 z 9 plansz; jeśli 9, to na każdej planszy, na której rozgrywka jeszcze się nie zakończyła
    std::vector<PBoard> localBoards;                // wektor 9 lokalnych plansz
    PBoard globalBoard;                             // globlana plansza

    public:
    GameState();        /**< Konstruktor. Tworzy strukturę danych reprezentującą nową rozgrywkę. */
    ~GameState();

    /** \brief  Metoda pozwalająca na "postawienie" kółka lub krzyżyka na danej planszy.
    *
    *   Zwraca true i zmienia wartości zmiennych lokalnych, jeśli operacja się powiedzie.
    *   @param board Numer wskazanej planszy.
    *   @param field Numer pola na wskazanej planszy.
    */
    bool makeMove(const int &board, const int &field);

    /** \brief  Metoda sprawdzająca czy ostatni ruch doprowadził do wygranej na planszy lokalnej. 
    *
    *   Zwraca symbol gracza, jeśli tak.\n
    *   W przeciwnym wypadku zwraca symbol NONE.
    */
    Board::PlayerSymbol checkLocalWin();

     /** \brief  Metoda sprawdzająca czy ostatni ruch doprowadził do wygranej na planszy globalnej. W przypadku remisu na danej planszy lokalnej "zajmowane" jest też pole na planszy globalnej.
    *
    *   Zwraca symbol gracza, jeśli tak.\n
    *   W przeciwnym wypadku zwraca symbol NONE.
    */
    Board::PlayerSymbol checkGlobalWin();

    /** \brief  Metoda zwracająca symbol gracza, który może w danej chwili wykonać ruch.
    */
    Board::PlayerSymbol getWhoseTurn();

    /** \brief  Metoda zwracająca informację czy na danej planszy nie można już wykonać żadnego ruchu. 
    *
    *   Zwraca true, jeśli nie można.
    *   @param board Numer sprawdzanej planszy.
    */
    bool isBoardNotPlayable(const int &board);

    /** \brief  Zwraca wartość zmiennej nextBoard. 
    *
    *   Jeśli wartość nextBoard należy do przedziału [0;8], to następny ruch może się odbyć na 1 z 9 plansz.\n
    *   Jeśli wartość nextBoard to 9, to następny ruch może się odbyć na każdej planszy, na której rozgrywka jeszcze się nie zakończyła.
    */
    int getNextBoard();

    /** \brief  Metoda zwracająca informację czy dana runda się zakończyła (remis lub wygrana).
    *
    *   Zwraca true, jeśli gra zakończona.\n
    */
    bool gameEnded();
};

#endif

