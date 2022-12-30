import random
import threading
import time
from threading import Thread

from pynput import mouse, keyboard


class AutoClicker:
    def __init__(self, shortcut, cycle, elastic=0):
        self.shortcut = shortcut
        self.cycle = cycle
        self.elastic = elastic

        self.perform = False

        self.mouse = mouse.Controller()

        self.daemon = None

    def on_press(self, key):
        if key == self.shortcut:
            print(threading.active_count())
            if self.perform:
                self.perform = False
            else:
                self.perform = True
                if self.daemon is None or not self.daemon.is_alive():
                    self.daemon = Thread(target=self.run)
                    self.daemon.start()

    def run(self):
        print('started')

        while self.perform:
            self.mouse.click(mouse.Button.left)

            time.sleep((self.cycle + random.uniform(-self.elastic, self.elastic)) / 1000)

        print('stopped')


if __name__ == '__main__':
    clicker = AutoClicker(keyboard.Key.shift_r, 200, 10)

    with keyboard.Listener(on_press=clicker.on_press) as listener:
        listener.join()
