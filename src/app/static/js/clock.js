/*
  Klasa reprezentująca stoper po stronie klienta.
*/
class Clock {
  /*
    konstruktor - tworzy nowy stoper
    args:
    timerTag - element htmlowy wyświetlający stan zegara
    timeLeft - czas na rozegranie rundy dla danego gracza
  */
  constructor(timerTag, timeLeft) {
    this.timerTag = timerTag;
    this.timeLeft = timeLeft;
    this.playTime = timeLeft;
    this.setHtml();
  }

  /*
    Przywraca stan początkowy zegara
  */
  reset = function() {
    this.timeLeft = this.playTime;
    this.setHtml();
  }

  /*
    aktualizuje pozostały czas na rundę dla danego gracza
    args:
    timeLeft - pozostały czas
  */
  setTimeLeft = function(timeLeft) {
    this.timeLeft = timeLeft;
  }

  /*
    pobiera czas pozostały na rundę dla danego gracza
  */
  getTimeLeft = function() {
    return this.timeLeft;
  }

  /*
    aktualizuje stan zegara w widoku u klienta
  */
  setHtml = function() {
    let minutes = parseInt(this.timeLeft / 60);
    let seconds = parseInt(this.timeLeft - minutes * 60);
    let time = (minutes < 10 ? '0' + minutes : minutes) + ':' + (seconds < 10 ? '0' + seconds : seconds);
    this.timerTag.html(time);
  }

  /*
    Funkcja wywołująca samą siebie rekurencyjnie za pośrednictwem funkcji startClock
    aktualizuje stan zegara w widoku u klienta i czas pozostały na rundę
  */
  countdown = function() {
    this.timeLeft -= 0.3;
    this.setHtml()
    if (this.timeLeft <= 0) return;
    this.startClock();
  }

  /*
    Wywołuje funkcję countdown z timeoutem 0.3s
  */
  startClock = function() {
    this.timer = setTimeout(this.countdown.bind(this), 300)
  }

  /*
    Czyści timeout
  */
  stopClock = function() {
    clearTimeout(this.timer);
  }
}
