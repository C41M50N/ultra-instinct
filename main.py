import multiprocessing
from pathlib import Path
from multiprocessing import Process, Value, Array, Queue
from typing import Any, Callable

from ultralytics import YOLO
from perception import detect, get_image, run_perception
from qvl.qcar import QLabsQCar

from onelap_w_perception import pid_controller
from pal.products.qcar import IS_PHYSICAL_QCAR


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")


def main(queue: multiprocessing.Queue):
    if not IS_PHYSICAL_QCAR:
        import setup_environment

        car = setup_environment.setup()  # Might need to move this to the main loop

    model = YOLO(model_path)

    while True:
        image = get_image(car, CAMERA)
        results = run_perception(model, image)
        obj = results.boxes.cls
        print(obj)
    # objs = detect(results)


if __name__ == "__main__":
    # Create a shared queue
    queue = multiprocessing.Queue()

    # Create the processes
    perception_process = multiprocessing.Process(target=main, args=(queue,))
    pid_controller_process = multiprocessing.Process(
        target=pid_controller, args=(queue,)
    )

    # Start the processes
    perception_process.start()
    pid_controller_process.start()

    # Wait for both processes to finish
    perception_process.join()
    pid_controller_process.join()
