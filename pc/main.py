import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

import multiprocessing
import time
import socket

import cv2
from pc.receive_n_perceive import main as receive_perceive_main
from pc.controller import main as controller_main


# def display_images(image_queue: multiprocessing.Queue):
#     while True:
#         img_display = image_queue.get()
#         cv2.imshow("YOLOv8 Detection", img_display)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     cv2.destroyAllWindows()


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    host = get_ip_address()
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        perception_queue = multiprocessing.Queue()

        recv_perceive = multiprocessing.Process(
            target=receive_perceive_main, args=(s, perception_queue)
        )
        control_send_process = multiprocessing.Process(
            target=controller_main, args=(perception_queue)
        )

        recv_perceive.start()
        control_send_process.start()

        # display_images(image_queue)

        recv_perceive.join()
        control_send_process.join()
