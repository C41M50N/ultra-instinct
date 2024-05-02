import multiprocessing
import time

from helper_funcs import (
    any_objects,
    get_height,
    queue_has_items,
    get_cls,
    get_perception,
    get_width,
    send_go,
    send_stop,
)
from enums import Cls


STOP_SIGN_MINIMUM_HEIGHT = 65


def main(perception_queue: multiprocessing.Queue, command_queue: multiprocessing.Queue):
    t1 = 0.0

    while True:
        if not perception_queue.empty():
            results = get_perception(perception_queue)

            if any_objects(results):
                cls = get_cls(results)

                if cls is Cls.STOP_SIGN:
                    height = get_height(results)
                    print(f"See: {cls.name}, height: {height:.2f}")

                    if height > STOP_SIGN_MINIMUM_HEIGHT:
                        send_stop(command_queue)
                        # wait for duration
                        t1 = time.time()
                        while time.time() - t1 <= 5:
                            if queue_has_items(perception_queue):
                                # consume unneeded observations
                                get_perception(perception_queue)
                        send_go(command_queue)

                        while True:
                            if queue_has_items(perception_queue):
                                results = get_perception(perception_queue)
                                # verify if there are any results to check
                                if any_objects(results):
                                    cls = get_cls(results)
                                    height = get_height(results)
                                    print(f"See2: {cls.name}, height: {height:.2f}")
                                    # If past the stop sign, start checking for new objects
                                    if (
                                        cls is not Cls.STOP_SIGN
                                        or cls is Cls.STOP_SIGN
                                        and height
                                        <= STOP_SIGN_MINIMUM_HEIGHT
                                        - STOP_SIGN_MINIMUM_HEIGHT * 0.1
                                    ):
                                        break

                elif cls is Cls.RED_LIGHT:
                    pass

                else:
                    print(f"See: {Cls.CLEAR.name}")
