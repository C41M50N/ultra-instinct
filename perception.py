from enum import IntEnum
import multiprocessing
from pathlib import Path
import multiprocessing
import time

import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results

from enums import STOP_CRITERIA, Cls, Command
from qvl.qcar import QLabsQCar
from pal.products.qcar import IS_PHYSICAL_QCAR


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")


def main(perception_queue: multiprocessing.Queue):
    print("Perception started...")

    if not IS_PHYSICAL_QCAR:
        import setup_environment

        car = setup_environment.setup()

    model = YOLO(model_path)

    while True:
        image = get_image(car, CAMERA)
        results = run_perception(model, image)
        perception_queue.put(results)

        # # If the model perceives an object(s)
        # if len(results.boxes.cls) > 0:
        #     width = float(results.boxes.xywh[0, 2])
        #     stop_criteria = STOP_CRITERIA[int(results.boxes.cls[0])]
        #     if stop_criteria.command is Command.STOP and width > stop_criteria.width:
        #         command_queue.put(stop_criteria)
        # else:
        #     # Sees clear roads
        #     stop_criteria = STOP_CRITERIA[Cls.CLEAR]
        #     command_queue.put(stop_criteria)


def parse_cls(results: Results):
    return [Cls(c) for c in results.boxes.cls.tolist()]


def get_image(car: QLabsQCar, camera: int) -> np.ndarray:
    return car.get_image(camera)[1]


def run_perception(model: YOLO, image: np.ndarray) -> Results:
    return model.predict(image, verbose=False)[0]
