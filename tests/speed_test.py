import timeit
from multiprocessing import Process, Queue, shared_memory
import numpy as np

timer = timeit.default_timer


# Custom class to use with the queue
class MyClass:
    def __init__(self, value: int):
        self.value = value


def queue_test(q: Queue, obj: MyClass):
    q.put(obj)
    obj_received = q.get()


def shared_memory_test(shm: shared_memory.SharedMemory, base_arr: np.ndarray):
    # Create shared memory and a NumPy array using that memory
    arr[:] = base_arr  # Initialize array
    # Simulate write and read
    arr[:] = arr[:] * 2  # Modify the array
    _ = arr[:]  # Read the array


queue_times = []
shared_memory_times = []

for _ in range(10000):
    # Time the queue test
    q = Queue()
    obj = MyClass(10)

    t1 = timer()
    queue_test(q, obj)
    t2 = timer()
    queue_times.append(t2 - t1)

    shm = shared_memory.SharedMemory(create=True, size=100)
    arr = np.ndarray((10,), dtype=np.int64, buffer=shm.buf)
    base_arr = np.arange(10)
    # Time the shared memory test
    t1 = timer()
    shared_memory_test(shm, base_arr)
    t2 = timer()
    shared_memory_times.append(t2 - t1)

    shm.close()
    shm.unlink()

avg_queue_time = sum(queue_times) / len(queue_times)
avg_shared_memory_time = sum(shared_memory_times) / len(shared_memory_times)

print(f"Queue time: {avg_queue_time}")
print(f"Shared Memory time: {avg_shared_memory_time}")
print(avg_queue_time / avg_shared_memory_time)
