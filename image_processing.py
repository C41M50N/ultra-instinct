import queue
import threading
from pathlib import Path

import cv2
import numpy as np
from qvl.qcar import QLabsQCar


def capture_images(
    queue: queue.Queue, car: QLabsQCar, camera: int, kill_signal: threading.Event
):
    img_num = 1
    while not kill_signal.is_set():
        front_img_raw = car.get_image(camera)[1]
        if front_img_raw is not None:
            queue.put((front_img_raw, img_num))
        else:
            print(f"No image captured at index {img_num}")
        img_num += 1


def save_images(
    queue: queue.Queue[np.ndarray], images_dir: Path, kill_signal: threading.Event
):
    while not kill_signal.is_set() or not queue.empty():
        if not queue.empty(): # wait for an image to be available
            front_img_raw, img_num = queue.get(timeout=1)
            # cv2.imshow("Camera Feed", front_img_raw)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            # cv2.imwrite(str(images_dir / f"{img_num}.jpg"), front_img_raw)
            queue.task_done()

    # cv2.destroyAllWindows()





def capture_images2(
    queue: queue.Queue, car: QLabsQCar, camera: int
):
    print("starting capture images process .......")
    img_num = 1
    while True:
        front_img_raw = car.get_image(camera)[1]
        if front_img_raw is not None:
            queue.put((front_img_raw, img_num))
        else:
            print(f"No image captured at index {img_num}")
        img_num += 1


def save_images2(
    queue: queue.Queue[np.ndarray], images_dir: Path
):
    print("starting display images process .......")
    while True:
        if not queue.empty(): # wait for an image to be available
            front_img_raw, img_num = queue.get(timeout=1)
            cv2.imshow("Camera Feed", front_img_raw)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # cv2.imwrite(str(images_dir / f"{img_num}.jpg"), front_img_raw)
            queue.task_done()

    cv2.destroyAllWindows()
