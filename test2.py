import multiprocessing
from multiprocessing import shared_memory, Semaphore, Lock
import numpy as np
import pickle
import struct
import random
import string
import time

QUEUE_SIZE = 10
BUFFER_SIZE = 1024  # Size per serialized Person object


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"Person({self.first_name}, {self.last_name})"


class SharedMemoryQueue:
    def __init__(self, name, buffer_size, queue_size, create=True):
        self.name = name
        self.buffer_size = buffer_size
        self.queue_size = queue_size

        if create:
            # Create shared memory block for queue
            self.shm = shared_memory.SharedMemory(
                create=True,
                size=(self.buffer_size + struct.calcsize("I")) * self.queue_size,
                name=f"{self.name}_queue",
            )
            self.queue = np.ndarray(
                (self.queue_size, self.buffer_size + struct.calcsize("I")),
                dtype=np.uint8,
                buffer=self.shm.buf,
            )

            # Create shared memory block for indices
            self.index_shm = shared_memory.SharedMemory(
                create=True, size=struct.calcsize("ii"), name=f"{self.name}_indices"
            )
            self.indices = np.ndarray((2,), dtype=np.int32, buffer=self.index_shm.buf)
            self.indices[0] = 0  # front
            self.indices[1] = 0  # rear
        else:
            # Open existing shared memory block for queue
            self.shm = shared_memory.SharedMemory(name=f"{self.name}_queue")
            self.queue = np.ndarray(
                (self.queue_size, self.buffer_size + struct.calcsize("I")),
                dtype=np.uint8,
                buffer=self.shm.buf,
            )

            # Open existing shared memory block for indices
            self.index_shm = shared_memory.SharedMemory(name=f"{self.name}_indices")
            self.indices = np.ndarray((2,), dtype=np.int32, buffer=self.index_shm.buf)

        # Initialize semaphores
        self.full_slots = Semaphore(0)
        self.empty_slots = Semaphore(self.queue_size)
        self.lock = Lock()

        self.full_count = multiprocessing.Value("i", 0)
        self.empty_count = multiprocessing.Value("i", self.queue_size)

    def put(self, obj):
        serialized = pickle.dumps(obj)
        if len(serialized) > self.buffer_size:
            raise ValueError("Object size exceeds buffer capacity!")

        self.empty_slots.acquire()
        with self.empty_count.get_lock():
            self.empty_count.value -= 1

        with self.lock:
            rear = self.indices[1]
            length_prefix = struct.pack("I", len(serialized))
            np.copyto(
                self.queue[rear, : len(length_prefix)],
                np.frombuffer(length_prefix, dtype=np.uint8),
            )
            np.copyto(
                self.queue[
                    rear, len(length_prefix) : len(length_prefix) + len(serialized)
                ],
                np.frombuffer(serialized, dtype=np.uint8),
            )
            self.indices[1] = (rear + 1) % self.queue_size

        with self.full_count.get_lock():
            self.full_count.value += 1
        self.full_slots.release()
        print(
            f"Queue Put | full_slots: {self.full_count.value}, empty_slots: {self.empty_count.value}"
        )

    def get(self):
        print(f"Queue Get | Waiting on full_slots...")
        self.full_slots.acquire()
        with self.full_count.get_lock():
            self.full_count.value -= 1

        with self.lock:
            front = self.indices[0]
            length_prefix = bytes(self.queue[front, : struct.calcsize("I")])
            length = struct.unpack("I", length_prefix)[0]
            data = bytes(
                self.queue[front, struct.calcsize("I") : struct.calcsize("I") + length]
            )
            self.indices[0] = (front + 1) % self.queue_size

        with self.empty_count.get_lock():
            self.empty_count.value += 1
        self.empty_slots.release()
        print(
            f"Queue Get | full_slots: {self.full_count.value}, empty_slots: {self.empty_count.value}"
        )
        return pickle.loads(data)

    def cleanup(self):
        self.shm.close()
        self.shm.unlink()
        self.index_shm.close()
        self.index_shm.unlink()


def generate_random_name(length=5):
    """Generate a random string of fixed length."""
    return "".join(
        random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length)
    )


def enqueue_persons(shm_queue_name, buffer_size, queue_size):
    shm_queue = SharedMemoryQueue(
        name=shm_queue_name,
        buffer_size=buffer_size,
        queue_size=queue_size,
        create=False,
    )

    while True:
        # Continuously generate and enqueue new persons
        first_name = generate_random_name()
        last_name = generate_random_name()
        person = Person(first_name, last_name)
        shm_queue.put(person)
        print(f"Enqueued person: {person}")
        time.sleep(1)  # Adjust the sleep time as needed


def dequeue_and_process_persons(shm_queue_name, buffer_size, queue_size):
    shm_queue = SharedMemoryQueue(
        name=shm_queue_name,
        buffer_size=buffer_size,
        queue_size=queue_size,
        create=False,
    )

    while True:
        person = shm_queue.get()
        print(f"Dequeued person: {person}")
        time.sleep(1)  # Adjust the sleep time as needed


def main():
    # Shared memory queue name
    shm_queue_name = "person_queue"

    # Initialize shared memory queue (creation should only happen here)
    shm_queue = SharedMemoryQueue(
        name=shm_queue_name, buffer_size=BUFFER_SIZE, queue_size=QUEUE_SIZE, create=True
    )

    # Start the enqueuing process
    producer_process = multiprocessing.Process(
        target=enqueue_persons, args=(shm_queue_name, BUFFER_SIZE, QUEUE_SIZE)
    )
    producer_process.start()

    # Start the consumer process
    consumer_process = multiprocessing.Process(
        target=dequeue_and_process_persons,
        args=(shm_queue_name, BUFFER_SIZE, QUEUE_SIZE),
    )
    consumer_process.start()

    try:
        producer_process.join()
        consumer_process.join()
    except KeyboardInterrupt:
        producer_process.terminate()
        consumer_process.terminate()
        producer_process.join()
        consumer_process.join()
        shm_queue.cleanup()


if __name__ == "__main__":
    main()
