from enum import IntEnum
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results
from qvl.qcar import QLabsQCar


class Objects(IntEnum):
    STOP_SIGN = 1
    RED_LIGHT = 2
    GREEN_LIGHT = 3


def get_image(car: QLabsQCar, camera: int) -> np.ndarray:
    return car.get_image(camera)[1]


def run_perception(model: YOLO, image: np.ndarray) -> Results:
    return model.predict(image, verbose=False)[0]


def detect(results: Results):
    """Returns the largest object found in the results"""
    None
