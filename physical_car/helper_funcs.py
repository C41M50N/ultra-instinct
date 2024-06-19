import multiprocessing
import socket

import numpy as np
from qvl.qcar import QLabsQCar
from pal.products.qcar import IS_PHYSICAL_QCAR

from enums import Cls, Command


def send_go(s: socket.socket):
    s.sendall(Command.GO)


def send_stop(s: socket.socket):
    s.sendall(Command.STOP)


def get_image(car: QLabsQCar, camera: int) -> np.ndarray:
    return car.get_image(camera)[1]


def get_command(queue: multiprocessing.Queue) -> Command:
    return queue.get()


def queue_has_items(queue: multiprocessing.Queue):
    return not queue.empty()
