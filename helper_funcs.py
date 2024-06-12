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


if not IS_PHYSICAL_QCAR:
    def parse_cls(results: Results):
        return [Cls(c) for c in results.boxes.cls.tolist()]


    def get_cls(results: Results):
        return Cls(int(results.boxes.cls[0]))

    def run_perception(model: YOLO, image: np.ndarray) -> Results:
        return model.predict(image, verbose=False)[0]


    def get_width(results: Results):
        return float(results.boxes.xywh[0, 2])


    def get_height(results: Results):
        return float(results.boxes.xywh[0, 3])


    def any_detected_objects(results: Results):
        return len(results.boxes.cls) > 0


    def get_perception(queue: multiprocessing.Queue) -> Results:
        return queue.get()


def get_image(car: QLabsQCar, camera: int) -> np.ndarray:
    return car.get_image(camera)[1]


def get_command(queue: multiprocessing.Queue) -> Command:
    return queue.get()


def queue_has_items(queue: multiprocessing.Queue):
    return not queue.empty()
