#ifndef BOARD_HPP
#define BOARD_HPP
#include <ostream>
class Board
{
    public:
    enum class PlayerSymbol {NONE=0, X, O};
    private:
    PlayerSymbol fields[9];      // plansza ma 9 pól; index=0 -> lewe górne pole; index=8 -> prawe dolne pole; 0-nic; 1-krzyżyk; 2-kółko
    int emptyFields;    // liczba wolnych pól
    bool end;           // fałsz, dopóki żaden z graczy nie wygrał i może wykonać ruchy
    PlayerSymbol winner;         // numer gracza, który wygrał (początkowo 0)

    PlayerSymbol isWin();        // metoda sprawdzająca czy wygrana; zwraca numer gracza lub 0 (gdy nikt nie wygrał)

    public:
    Board();
    ~Board();

    bool isPickPossible(const int &field);               // metoda sprawdzająca czy możliwe jest "postawienie" kółka lub krzyżyka; zwraca true, jeśli operacja się powiedzie
    bool pickField(const int &field, const PlayerSymbol &player); // metoda pozwalająca na "postawienie" kółka lub krzyżyka; zwraca true, jeśli operacja się powiedzie
    bool gameEnded();                                    // metoda sprawdzająca czy gra na danej planszy została zakończona
    PlayerSymbol getWinner();                                     // metoda zwracające numer gracza, który wygrał na planszy (lub 0, gdy żaden)
};
static inline std::ostream& operator<<(std::ostream& os, const Board::PlayerSymbol& ps) 
{
    return os << static_cast<int>(ps);
}
#endif