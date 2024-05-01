import multiprocessing
from pathlib import Path
import multiprocessing

from ultralytics import YOLO

from helper_funcs import get_image, run_perception, send_results
from qvl.qcar import QLabsQCar
from pal.products.qcar import IS_PHYSICAL_QCAR


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")


def main(perception_queue: multiprocessing.Queue):
    if not IS_PHYSICAL_QCAR:
        import setup_environment

        car = setup_environment.setup()

    model = YOLO(model_path)

    while True:
        image = get_image(car, CAMERA)
        results = run_perception(model, image)
        send_results(perception_queue, results)
