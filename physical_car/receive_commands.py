import multiprocessing
import socket


def receive_commands(conn: socket.socket, command_queue: multiprocessing.Queue):
    while True:
        command = conn.recv(4)
        print(command)
        command_queue.put(command)


if __name__ == "__main__":
    # Example usage
    receive_commands("172.23.141.56", 12345)
    # receive_img("192.168.2.12", 12345)
