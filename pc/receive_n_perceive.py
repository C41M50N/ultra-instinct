from io import BytesIO
import os
import socket
import timeit
import numpy as np
import cv2
import multiprocessing
from helper_funcs import run_perception
from pal.products.qcar import QCarRealSense
from PIL import Image

# Prime the camera and compression algo for faster running later
timer = timeit.default_timer
camera = QCarRealSense("rgb", frameWidthRGB=640, frameHeightRGB=480)
camera.read_RGB()
img: np.ndarray = camera.imageBufferRGB
_, encoded_image = cv2.imencode(".png", img)  # compression ~ 6x
model = YOLO(model_path)


def receive_perceive(s: socket.socket, queue: multiprocessing.Queue):
    while True:
        # Receive the length of the PNG data
        length = int.from_bytes(conn.recv(4), "big")

        # Receive the PNG data
        png_data = b""
        while len(png_data) < length:
            packet = conn.recv(length - len(png_data))
            if not packet:
                break
            png_data += packet

        image = Image.open(BytesIO(png_data))
        image.show()
        # image_np = np.array(image)

        results = run_perception(model, image)
        queue.put(results)

    # print(msg)


def main():
    receive_perceive("172.23.141.56", 12345)


if __name__ == "__main__":
    main()
    # receive_perceive("172.23.141.56", 12345)
    # send_img("192.168.2.12", 12345)
