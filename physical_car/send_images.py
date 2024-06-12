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
        print("1")
        camera.read_RGB()
        print("2")
        img: np.ndarray = camera.imageBufferRGB
        print("3")
        _, encoded_image = cv2.imencode(".png", img)
        print("4")
        png_data = encoded_image.tobytes()
        print("5")

        s.sendall(len(png_data).to_bytes(4, "big"))
        print("6")
        s.sendall(png_data)


if __name__ == "__main__":
    send_images("172.23.141.56", 12345)
    # send_img("192.168.2.12", 12345)
