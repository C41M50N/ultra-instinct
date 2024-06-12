from io import BytesIO
import multiprocessing
import socket

import cv2
import numpy as np
from PIL import Image


def adjust_image(img: np.ndarray) -> np.ndarray:
    # Convert image to float32 for manipulation
    img_float = img.astype(np.float32)

    # Reduce the green channel intensity
    img_float[:, :, 1] *= 0.75  # Adjust the factor as needed to reduce green

    # Increase brightness
    img_float += 90  # Increase brightness by 50 units

    # Clip the values to be in the valid range [0, 255]
    img_float = np.clip(img_float, 0, 255)

    # Convert image back to uint8
    adjusted_img = img_float.astype(np.uint8)

    return adjusted_img


def receive_commands(conn: socket.socket, command_queue: multiprocessing.Queue):
    while True:
        command = conn.recv(4)
        command_queue.put(command)


if __main__ == "__main__":
    # Example usage
    receive_commands("172.23.141.56", 12345)
    # receive_img("192.168.2.12", 12345)
