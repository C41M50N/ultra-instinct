import multiprocessing
import time

from helper_funcs import (
    any_objects,
    queue_has_items,
    get_cls,
    get_perception,
    get_width,
    send_go,
    send_stop,
)
from enums import Cls

STOP_SIGN_MINIMUM_DISTANCE = 70


def main(perception_queue: multiprocessing.Queue, command_queue: multiprocessing.Queue):
    t1 = 0.0

    while True:
        if not perception_queue.empty():
            results = get_perception(perception_queue)

            if any_objects(results):
                cls = get_cls(results)
                width = get_width(results)
                print(f"See: {cls.name}, width: {width}")

                if cls is Cls.STOP_SIGN and width > STOP_SIGN_MINIMUM_DISTANCE:
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
                                width = get_width(results)
                                # If past the stop sign, start checking for new objects
                                if (
                                    cls is not Cls.STOP_SIGN
                                    or cls is Cls.STOP_SIGN
                                    and width <= STOP_SIGN_MINIMUM_DISTANCE
                                ):
                                    break

                elif cls is Cls.RED_LIGHT:
                    pass

                # elif cls is Cls.GREEN_LIGHT:
                #     pass

                prev_cls = cls
