from io import BytesIO
import socket
import numpy as np
import cv2

from PIL import Image

import timeit

timer = timeit.default_timer


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


def receive_img(host, port):
    # Create a socket connection
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    # Receive the length of the PNG data
                    length = int.from_bytes(conn.recv(4), "big")

                    # Receive the PNG data
                    png_data = b""
                    while len(png_data) < length:
                        packet = conn.recv(length - len(png_data))
                        if not packet:
                            break
                        png_data += packet

                    conn.sendall(b"what up!")

                    image = Image.open(BytesIO(png_data))
                    image_np = np.array(image)

                    # Adjust the image
                    t1 = timer()
                    adjusted_image_np = adjust_image(image_np)
                    t2 = timer()
                    print((t2 - t1) * 10)
                    # Convert back to PIL Image to display
                    adjusted_image = Image.fromarray(adjusted_image_np)
                    adjusted_image.show()
        except Exception as e:
            print(f"error! {e}")


# Example usage
receive_img("172.23.141.56", 12345)
# receive_img("192.168.2.12", 12345)
