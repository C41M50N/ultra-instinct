import multiprocessing
import time

from helper_funcs import (
    any_detected_objects,
    get_height,
    queue_has_items,
    get_cls,
    get_perception,
    get_width,
    send_go,
    send_stop,
)
from enums import Cls


STOP_SIGN_MINIMUM_HEIGHT = 64
RED_LIGHT_MINIMUM_WIDTH = 22
STOP_SIGN_DURATION = 3


def main(perception_queue: multiprocessing.Queue, command_queue: multiprocessing.Queue):
    while True:
        if not perception_queue.empty():
            results = get_perception(perception_queue)

            if any_detected_objects(results):
                cls = get_cls(results)

                if cls is Cls.STOP_SIGN:
                    height = get_height(results)
                    print(f"Controller: {cls.name}, height: {height:.1f}")

                    if height > STOP_SIGN_MINIMUM_HEIGHT:
                        send_stop(command_queue)
                        # wait for duration
                        t1 = time.time()
                        while time.time() - t1 <= STOP_SIGN_DURATION:
                            if queue_has_items(perception_queue):
                                # consume unneeded observations
                                get_perception(perception_queue)
                        send_go(command_queue)

                        while True:
                            if queue_has_items(perception_queue):
                                results = get_perception(perception_queue)
                                # verify if there are any results to check
                                if any_detected_objects(results):
                                    cls = get_cls(results)
                                    height = get_height(results)
                                    # print(
                                    #     f"Controller: debug {cls.name}, height: {height:.1f}"
                                    # )
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
                    width = get_width(results)
                    print(f"Controller: {cls.name}, width: {width:.1f}")

                    if width > RED_LIGHT_MINIMUM_WIDTH:
                        send_stop(command_queue)

                        while True:
                            if queue_has_items(perception_queue):
                                results = get_perception(perception_queue)
                                if any_detected_objects(results):
                                    cls = get_cls(results)
                                    if cls is Cls.GREEN_LIGHT:
                                        send_go(command_queue)
                                        break
                                else:
                                    # This should never run. it means the model can't see any traffic signals when it needs to be watching for a green light
                                    print("ERROR: bad")
            # else:
            #     print(f"Controller: {Cls.CLEAR.name}")
