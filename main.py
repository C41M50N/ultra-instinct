from enum import IntEnum
import multiprocessing
from pathlib import Path

from ultralytics import YOLO
from qvl.qcar import QLabsQCar

from onelap_w_perception import pid_controller
from pal.products.qcar import IS_PHYSICAL_QCAR
from perception import get_image, parse_cls, run_perception


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")


class Command(IntEnum):
    STOP = 1
    GO = 2


def main(queue: multiprocessing.Queue):
    if not IS_PHYSICAL_QCAR:
        import setup_environment

        car = setup_environment.setup()

    model = YOLO(model_path)

    while True:
        image = get_image(car, CAMERA)
        results = run_perception(model, image)
        cls = parse_cls(results)
        print([c.name for c in cls])


if __name__ == "__main__":
    queue = multiprocessing.Queue()

    perception_process = multiprocessing.Process(target=main, args=(queue,))
    pid_controller_process = multiprocessing.Process(
        target=pid_controller, args=(queue,)
    )

    perception_process.start()
    pid_controller_process.start()

    perception_process.join()
    pid_controller_process.join()
