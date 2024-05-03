from enum import IntEnum
import multiprocessing

import keyboard
from enums import ArrowKey


def main(keyboard_queue: multiprocessing.Queue):
    def on_press(key):
        if key.name == "left":
            keyboard_queue.put(ArrowKey.LEFT)
        elif key.name == "right":
            keyboard_queue.put(ArrowKey.RIGHT)
        elif key.name == "up":
            keyboard_queue.put(ArrowKey.UP)
        elif key.name == "down":
            keyboard_queue.put(ArrowKey.DOWN)

    keyboard.on_press(
        on_press#, suppress=True
    )  # suppress=True to prevent key from being sent to other programs

    # Keep the listener running
    keyboard.wait()
