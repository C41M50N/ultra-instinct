import multiprocessing
import time


def main(perception_queue: multiprocessing.Queue, command_queue: multiprocessing.Queue):
    while True:
        print("Controller!")
        time.sleep(1)
