import multiprocessing
import time

import cv2

from environment import main as environment_main
from perception import main as perception_main
from controller import main as controller_main
from pid_controller import main as pid_controller_main


def display_images(image_queue: multiprocessing.Queue):
    while True:
        img_display = image_queue.get()
        cv2.imshow("YOLOv8 Detection", img_display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    perception_queue = multiprocessing.Queue()
    command_queue = multiprocessing.Queue()
    image_queue = multiprocessing.Queue()

    environment_process = multiprocessing.Process(target=environment_main)
    perception_process = multiprocessing.Process(
        target=perception_main, args=(perception_queue, image_queue)
    )
    controller_process = multiprocessing.Process(
        target=controller_main, args=(perception_queue, command_queue)
    )
    pid_controller_process = multiprocessing.Process(
        target=pid_controller_main, args=(command_queue,)
    )

    environment_process.start()
    time.sleep(2)
    perception_process.start()
    controller_process.start()
    time.sleep(4)
    pid_controller_process.start()

    display_images(image_queue)

    environment_process.join()
    perception_process.join()
    controller_process.join()
    pid_controller_process.join()
