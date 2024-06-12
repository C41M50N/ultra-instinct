from io import BytesIO
from pathlib import Path
import multiprocessing
import socket

from ultralytics import YOLO
from helper_funcs import run_perception
from PIL import Image


model_path = Path("models/best5.pt")
model = YOLO(model_path)


def receive_perceive(s: socket.socket, queue: multiprocessing.Queue):
    while True:
        # Receive the length of the PNG data
        length = int.from_bytes(s.recv(4), "big")

        # Receive the PNG data
        png_data = b""
        while len(png_data) < length:
            packet = s.recv(length - len(png_data))
            if not packet:
                break
            png_data += packet

        image = Image.open(BytesIO(png_data))
        # image.show()
        # image_np = np.array(image)

        results = run_perception(model, image)
        queue.put(results)


if __name__ == "__main__":
    receive_perceive("172.23.141.56", 12345)
    # send_img("192.168.2.12", 12345)
