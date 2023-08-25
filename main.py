import logging
import random
import threading
import time

from pynput import mouse, keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoClicker(threading.Thread):
    def __init__(self, shortcut, interval, elastic=0):
        super().__init__()

        self.shortcut = shortcut
        self.interval = interval
        self.elastic = elastic

        self.exit = False
        self.click = False

        self.mouse = mouse.Controller()

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def run(self) -> None:
        while True:
            time.sleep((self.interval + random.uniform(-self.elastic, self.elastic)) / 1000)

            if self.exit:
                return

            if self.click:
                self.mouse.click(mouse.Button.left)

    def on_press(self, key):
        if key == self.shortcut:
            if self.click:
                logger.info('Stop clicking.')
                self.click = False
            else:
                logger.info('Start clicking.')
                self.click = True
            return

        if key == keyboard.Key.esc:
            logger.info('Quitting clicker.')
            self.exit = True
            return


if __name__ == '__main__':
    clicker = AutoClicker(keyboard.Key.shift_r, 200, 10)
    clicker.start()
