class Clock {
  constructor(timerTag, timeLeft) {
    this.timerTag = timerTag;
    this.timeLeft = timeLeft;
    this.playTime = timeLeft;
    this.setHtml();
  }
  reset = function() {
    this.timeLeft = this.playTime;
  }
  setTimeLeft = function(timeLeft) {
    this.timeLeft = timeLeft;
  }
  getTimeLeft = function() {
    return this.timeLeft;
  }
  setHtml = function() {
    let minutes = parseInt(this.timeLeft / 60);
    let seconds = parseInt(this.timeLeft - minutes * 60);
    let time = (minutes < 10 ? '0' + minutes : minutes) + ':' + (seconds < 10 ? '0' + seconds : seconds);
    this.timerTag.html(time);
  }
  countdown = function() {
    console.log(this)
    this.timeLeft -= 1;
    this.setHtml()
    if (this.timeLeft <= 0) return;
    this.startClock();
  }
  startClock = function() {
    console.log(this.timerTag.html);
    this.timer = setTimeout(this.countdown.bind(this), 1000)
  }
  stopClock = function() {
    clearTimeout(this.timer);
  }
}
