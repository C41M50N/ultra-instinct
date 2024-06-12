import multiprocessing
import socket
from pc.controller import main as controller_main
from physical_car.send_images import send_images
from physical_car.pid_controller import main as pid_controller_main


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    host = get_ip_address()
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            command_queue = multiprocessing.Queue()

            # environment_process = multiprocessing.Process(target=environment_main)
            image_send_process = multiprocessing.Process(
                target=send_images, args=(conn)
            )
            command_receive_process = multiprocessing.Process(
                target=controller_main, args=(conn, command_queue)
            )
            pid_controller_process = multiprocessing.Process(
                target=pid_controller_main, args=(command_queue,)
            )

            image_send_process.start()
            command_receive_process.start()
            pid_controller_process.start()

            # display_images(image_queue)

            image_send_process.join()
            controller_process.join()
            pid_controller_process.join()
