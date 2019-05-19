#ifndef BOARD_HPP
#define BOARD_HPP
#include <ostream>

/** \file Board.hpp
*   \brief Plik nagłówkowy zawierający definicję klasy "Board" oraz klasy enum "PlayerSymbol".
*/


/*! \brief Klasa reprezentująca pojedyńczą planszę. Posiada metody pozwalajace na obsłużenie klasycznej gry w kółko i krzyżyk (np. zajmowanie pola przez symbol, sprawdzanie wygranej).
*
*   Używana jako reprezentacja planszy w skali mikro oraz makro.\n
*   Plansza makro składa się z 9 plansz.\n
*/
class Board
{
    public:
    /** 
    *   Typ enum reprezentujący puste pole oraz symbole służące do zajmowania pól przez graczy.
    */
    enum class PlayerSymbol 
    {
        NONE=0,     /**< symbol reprezentujący puste pole */
        X,          /**< symbol używany przez gracza 1*/
        O           /**< symbol używany przez gracza 2*/
    };

    private:
    PlayerSymbol fields[9];      // plansza ma 9 pól; index=0 -> lewe górne pole; index=8 -> prawe dolne pole
    int emptyFields;             // liczba wolnych pól
    bool end;                    // fałsz, dopóki żaden z graczy nie wygrał i może wykonać ruchy
    PlayerSymbol winner;         // numer gracza, który wygrał (początkowo 0)
    PlayerSymbol isWin();        // metoda sprawdzająca czy wygrana; zwraca numer gracza lub 0 (gdy nikt nie wygrał)

    public:
    Board();    /**< Konstruktor. Tworzy "czystą" planszę do rozgrywki. */
    ~Board();

    /** \brief  Metoda sprawdzająca czy możliwe jest "postawienie" kółka lub krzyżyka na danym polu. 
    *
    *   Zwraca true, jeśli operacja się powiedzie.
    *   @param field Numer sprawdzanego pola.
    */
    bool isPickPossible(const int &field);

    /** \brief  Metoda pozwalająca na "postawienie" kółka lub krzyżyka.
    *
    *   W przypadku, gdy następny ruch na danej planszy jest niemożliwy z powodu remisu lub wygranej, metoda ustawia odpowiednie zmienne informujące o wyniku rozgrywki na danej planszy.\n
    *   Zwraca true, jeśli operacja się powiedzie.
    *   @param field Numer pola.
    *   @param player Symbol gracza wykonującego ruch.
    */
    bool pickField(const int &field, const PlayerSymbol &player);

    /** \brief  Metoda sprawdzająca czy gra na danej planszy została zakończona.
    *
    *   Zwraca true, jeśli tak.
    */   
    bool gameEnded();

    /** \brief Metoda zwracająca symbol gracza, który wygrał na planszy.
    */      
    PlayerSymbol getWinner();
};

static inline std::ostream& operator<<(std::ostream& os, const Board::PlayerSymbol& ps) 
{
    return os << static_cast<int>(ps);
}
#endif