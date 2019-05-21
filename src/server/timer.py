#!venv/bin/python3
## \file timer.py
#  Plik zawierający definicję klasy "Timer"
import time

## Klasa reprezentująca zegar odmierzający pozostały czas rozgrywki dla danego gracza.
class Timer:
    ## Konstruktor. Tworzy nowy zegar. Ustawia pozostały czas (timeLeft) na wartość
    #  podaną jako parametr.
    #  @param self
    #  @param seconds - czas na pojedynczą grę dla jednego gracza.
    def __init__(self, seconds):
        self.startTime = None
        self.timeLeft = seconds
    ## Uruchamia zegar (ustawia moment początkowy)
    #  @param self
    def start(self):
        self.startTime = time.time()
    ## Zatrzymuje zegar (aktualizuje pozostały czas na rozgrywkę dla danego gracza
    #  odejmując od pozostałego czasu różnicę czasu między chwilą obecną a momentem początkowym)<br>
    #  Gdy Timer.stop zostanie wywołane bez uprzedniego wywołania Timer.start, wówczas
    #  funkcja obsługuje wyjątek i wyświetla komunikat w konsoli.
    #  @param self
    def stop(self):
        try:
            self.timeLeft = self.timeLeft - (time.time() - self.startTime)
            self.startTime = None
        except TypeError:
            print('Przed wyywołaniem metody Timer.stop należy wywołać metodę Timer.start...')
    ## Sprawdza czy gracz, dla którego obiekt odmierza czas nie przekroczył maksymalnego
    #  czasu rozgrywki przeznaczonego dla jednego gracza.
    ## Zwraca:<br>
    #  True - kiedy gracz przekroczył zadany czas<br>
    #  False - w przeciwnym przypadku
    # @param self
    def check(self):
        return self.timeLeft <= 0
