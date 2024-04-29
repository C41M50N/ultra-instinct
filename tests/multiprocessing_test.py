from multiprocessing import shared_memory, Process
import numpy as np


def modify_array(shm_name, shape):
    # Attach to the existing shared memory block
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    # Create a NumPy array from the shared memory
    arr = np.ndarray(shape, dtype=np.int64, buffer=existing_shm.buf)
    arr += 1  # Modify the array


if __name__ == "__main__":
    # Create a shared NumPy array
    original_data = np.array([1, 2, 3, 4, 5], dtype=np.int64)
    shm = shared_memory.SharedMemory(create=True, size=original_data.nbytes)
    arr = np.ndarray(original_data.shape, dtype=np.int64, buffer=shm.buf)
    arr[:] = original_data[:]  # Copy data into shared memory

    # Create and start a process
    p = Process(target=modify_array, args=(shm.name, arr.shape))
    p.start()
    p.join()

    # Print the modified array
    print(f"Orignal array: {original_data[:]}")
    print(f"Modified array: {arr[:]}")
    # Clean up shared memory
    shm.close()
    shm.unlink()


print()


from multiprocessing import Process, Value, Array, Queue


def modify_shared_data(n, arr):
    n.value = 3.14159  # Modify the shared value
    for i in range(len(arr)):
        arr[i] = arr[i] ** 2  # Square each element in the shared array


if __name__ == "__main__":
    # Create a shared double value
    num = Value("d", 0.0)
    # Create a shared array of integers
    arr = Array("i", range(5))

    # Print initial values
    print(f"Initial value: {num.value}")
    print(f"Initial array: {arr[:]}")

    # Create and start a process that modifies shared data
    p = Process(target=modify_shared_data, args=(num, arr))
    p.start()
    p.join()

    # Print modified values
    print(f"Modified value: {num.value}")
    print(f"Modified array: {arr[:]}")
