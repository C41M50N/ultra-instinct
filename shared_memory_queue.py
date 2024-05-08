import multiprocessing
from multiprocessing import shared_memory, Semaphore, Lock
import numpy as np
from ultralytics import YOLO  # Assuming this is your YOLO model import
from ultralytics.engine.results import Results
import pickle
import struct
import ctypes

QUEUE_SIZE = 10
BUFFER_SIZE = 1024 * 1024  # Example size per Results object


class SharedMemoryQueue:
    def __init__(self, name: str, buffer_size: int, queue_size: int):
        self.name = name
        self.buffer_size = buffer_size
        self.queue_size = queue_size

        # Create shared memory block
        self.shm = shared_memory.SharedMemory(
            create=True, size=self.buffer_size * self.queue_size
        )
        self.queue = np.ndarray(
            (self.queue_size, self.buffer_size), dtype=np.uint8, buffer=self.shm.buf
        )

        # Initialize queue pointers and semaphores
        self.index_shm = shared_memory.SharedMemory(
            create=True, size=struct.calcsize("ii")
        )
        self.indices = np.ndarray((2,), dtype=np.int32, buffer=self.index_shm.buf)
        self.indices[0] = 0  # front
        self.indices[1] = 0  # rear
        self.full_slots = Semaphore(0)
        self.empty_slots = Semaphore(self.queue_size)
        self.lock = Lock()

    def put(self, obj: Results):
        serialized = pickle.dumps(obj)
        if len(serialized) > self.buffer_size:
            raise ValueError("Object size exceeds buffer capacity!")

        self.empty_slots.acquire()
        with self.lock:
            rear = self.indices[1]
            np.copyto(
                self.queue[rear, : len(serialized)],
                np.frombuffer(serialized, dtype=np.uint8),
            )
            self.indices[1] = (rear + 1) % self.queue_size
        self.full_slots.release()

    def get(self):
        self.full_slots.acquire()
        with self.lock:
            front = self.indices[0]
            data = bytes(self.queue[front, :])
            self.indices[0] = (front + 1) % self.queue_size
        self.empty_slots.release()
        return pickle.loads(data)

    def cleanup(self):
        self.shm.close()
        self.shm.unlink()
        self.index_shm.close()
        self.index_shm.unlink()


def run_perception_and_enqueue(
    model, shm_queue_name, buffer_size, queue_size, car, camera
):
    shm_queue = SharedMemoryQueue(
        name=shm_queue_name, buffer_size=buffer_size, queue_size=queue_size
    )

    while True:
        image = get_image(car, camera)
        results = run_perception(model, image)
        shm_queue.put(results)


def dequeue_and_process(shm_queue_name, buffer_size, queue_size):
    shm_queue = SharedMemoryQueue(
        name=shm_queue_name, buffer_size=buffer_size, queue_size=queue_size
    )

    while True:
        results = shm_queue.get()
        print(f"Received results: {results}")


def main():
    # Set up YOLO model and camera
    car = setup_car()
    model = YOLO("yolov8s.pt")  # Replace with your model
    camera = "CAMERA"  # Replace with your actual camera constant

    # Shared memory queue name
    shm_queue_name = "results_queue"

    # Initialize shared memory queue
    shm_queue = SharedMemoryQueue(
        name=shm_queue_name, buffer_size=BUFFER_SIZE, queue_size=QUEUE_SIZE
    )

    # Start the perception process
    perception_process = multiprocessing.Process(
        target=run_perception_and_enqueue,
        args=(model, shm_queue_name, BUFFER_SIZE, QUEUE_SIZE, car, camera),
    )
    perception_process.start()

    # Start the consumer process
    consumer_process = multiprocessing.Process(
        target=dequeue_and_process, args=(shm_queue_name, BUFFER_SIZE, QUEUE_SIZE)
    )
    consumer_process.start()

    try:
        perception_process.join()
        consumer_process.join()
    except KeyboardInterrupt:
        perception_process.terminate()
        consumer_process.terminate()
        perception_process.join()
        consumer_process.join()
        shm_queue.cleanup()


if __name__ == "__main__":
    main()
