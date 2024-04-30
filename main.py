import multiprocessing

from perception import main as perception_main
from controller import main as controller_main
from pid_controller import main as pid_controller_main


if __name__ == "__main__":
    perception_queue = multiprocessing.Queue()
    command_queue = multiprocessing.Queue()

    perception_process = multiprocessing.Process(
        target=perception_main, args=(perception_queue,)
    )
    controller_process = multiprocessing.Process(
        target=controller_main, args=(perception_queue, command_queue)
    )
    pid_controller_process = multiprocessing.Process(
        target=pid_controller_main, args=(command_queue,)
    )

    perception_process.start()
    controller_process.start()
    pid_controller_process.start()

    perception_process.join()
    controller_process.join()
    pid_controller_process.join()
