import os
import socket

import cv2
import numpy as np
from pal.products.qcar import QCarRealSense

# Prime the camera and compression algo for speedup later
camera = QCarRealSense("rgb", frameWidthRGB=640, frameHeightRGB=480)
camera.read_RGB()
img: np.ndarray = camera.imageBufferRGB
_, encoded_image = cv2.imencode(".png", img)


def send_images(s: socket.socket):
    while True:
        camera.read_RGB()
        img: np.ndarray = camera.imageBufferRGB
        _, encoded_image = cv2.imencode(".png", img)
        png_data = encoded_image.tobytes()

        s.sendall(len(png_data).to_bytes(4, "big"))
        s.sendall(png_data)


if __name__ == "__main__":
    send_images("172.23.141.56", 12345)
    # send_img("192.168.2.12", 12345)
