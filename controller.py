import multiprocessing


def main(perception_queue: multiprocessing.Queue, command_queue: multiprocessing.Queue):
    print("Controller started...")

    while True:
        if not perception_queue.empty():
            print(perception_queue.get())
