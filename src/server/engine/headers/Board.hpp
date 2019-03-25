#ifndef BOARD_HPP
#define BOARD_HPP

class Board
{
    int fields[9];      // plansza ma 9 pól; index=0 -> lewe górne pole; index=8 -> prawe dolne pole; 0-nic; 1-krzyżyk; 2-kółko
    int emptyFields;    // liczba wolnych pól
    bool end;           // fałsz, dopóki żaden z graczy nie wygrał i może wykonać ruchy
    int winner;         // numer gracza, który wygrał (początkowo 0)

    int isWin();        // metoda sprawdzająca czy wygrana; zwraca numer gracza lub 0 (gdy nikt nie wygrał)

    public:
    Board();
    ~Board();

    bool isPickPossible(const int &field);               // metoda sprawdzająca czy możliwe jest "postawienie" kółka lub krzyżyka; zwraca true, jeśli operacja się powiedzie
    bool pickField(const int &field, const int &player); // metoda pozwalająca na "postawienie" kółka lub krzyżyka; zwraca true, jeśli operacja się powiedzie
    bool gameEnded();                                    // metoda sprawdzająca czy gra na danej planszy została zakończona
    int getWinner();                                     // metoda zwracające numer gracza, który wygrał na planszy (lub 0, gdy żaden)
};

#endif