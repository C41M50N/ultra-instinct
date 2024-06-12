import os
import socket

import numpy as np
import cv2
from pal.products.qcar import QCarRealSense


def setup_car(host: str, port: int):
    os.system("cls")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.listen()
        conn, addr = s.accept()

        camera = QCarRealSense("RGB", frameWidthRGB=640, frameHeightRGB=480)
        camera.read_RGB()
        img: np.ndarray = camera.imageBufferRGB
        _, encoded_image = cv2.imencode(".png", img)
        png_data = encoded_image.tobytes()
        
        conn.sendall(len(png_data).to_bytes(4, "big"))
        conn.sendall(png_data)
        print("sent!")


if __name__ == "__main__":
    setup_car()
