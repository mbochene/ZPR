#!venv/bin/python3
import time


class Timer:
    def __init__(self, seconds):
        self.startTime = None
        self.timeLeft = seconds

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.timeLeft = self.timeLeft - (time.time() - self.startTime)
        self.startTime = time.time()

    def check(self):
        return self.timeLeft <= 0
