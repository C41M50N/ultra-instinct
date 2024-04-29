from pathlib import Path
import queue
import threading

import numpy as np
from PIL import Image
from qvl.qcar import QLabsQCar
from ultralytics import YOLO
from ultralytics.engine.results import Results


def capture_image(
    car: QLabsQCar,
    queue: queue.Queue,
    kill_signal: threading.Event,
    camera: QLabsQCar,
    model: YOLO,
):
    img_num = 1
    while not kill_signal.is_set():
        try:
            front_img_raw = car.get_image(camera)[1]
            if front_img_raw is not None:
                queue.put((front_img_raw, img_num))
            else:
                print(f"No image captured at index {img_num}")
            img_num += 1
        except Exception as e:
            print(f"Error capturing image at index {img_num}: {e}")


def save_images(
    queue: queue.Queue[np.ndarray], kill_signal: threading.Event, images_dir: Path
):
    while not kill_signal.is_set() or not queue.empty():
        try:
            # wait for an image to be available
            front_img_raw, img_num = queue.get(timeout=1)
            front_img = Image.fromarray(front_img_raw)
            img_path = images_dir / f"{img_num}.png"
            front_img.save(img_path)
            queue.task_done()
        except queue.empty():
            continue
        except Exception as e:
            print(f"Error saving image {img_num}: {e}")
