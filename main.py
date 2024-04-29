import multiprocessing
from pathlib import Path
from dataclasses import dataclass

from PIL import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results
from qvl.qcar import QLabsQCar

from enums import Command
from onelap_w_perception import pid_controller
from pal.products.qcar import IS_PHYSICAL_QCAR
from perception import get_image, parse_cls, run_perception
from perception import Cls


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")


def get_box_size(results: Results):
    None


@dataclass
class StopCriteria:
    cls: Cls
    width: float
    time: float


STOP_CRITERIA = {
    0: StopCriteria(Cls.STOP_SIGN, 70, 5),
    1: StopCriteria(Cls.RED_LIGHT, 10, float("inf")),
    2: StopCriteria(Cls.GREEN_LIGHT, 10, float("inf")),
}


def main(command_queue: multiprocessing.Queue):
    if not IS_PHYSICAL_QCAR:
        import setup_environment

        car = setup_environment.setup()

    model = YOLO(model_path)

    while True:
        image = get_image(car, CAMERA)
        results = run_perception(model, image)
        if len(results.boxes.cls) > 0:
            width = float(results.boxes.xywh[0, 2])
            print(width)
            stop_criteria: StopCriteria = STOP_CRITERIA[int(results.boxes.cls[0])]

            # results.save("output.png")

            if (
                stop_criteria.cls in {Cls.STOP_SIGN, Cls.RED_LIGHT}
                and width > stop_criteria.width
            ):
                command_queue.put(Command.STOP)

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
