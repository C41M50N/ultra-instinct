import multiprocessing
import os
from pathlib import Path
import multiprocessing

from ultralytics import YOLO
from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.qcar import QLabsQCar
from qvl.real_time import QLabsRealTime

from helper_funcs import get_image, run_perception, send_results
import pal.resources.rtmodels as rtmodels


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")


def main(perception_queue: multiprocessing.Queue):
    car = setup_car()

    model = YOLO(model_path)

    while True:
        image = get_image(car, CAMERA)
        results = run_perception(model, image)
        send_results(perception_queue, results)


def setup_car():
    os.system("cls")

    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    initialPosition = [-1.205, -0.83, 0.005]
    initialOrientation = [0, 0, -44.7]
    # Spawn a QCar at the given initial pose
    qcar = QLabsQCar(qlabs)
    qcar.spawn_id(
        actorNumber=0,
        location=[p * 10 for p in initialPosition],
        rotation=initialOrientation,
        waitForConfirmation=True,
    )

    # Create a new camera view and attach it to the QCar
    hcamera = QLabsFreeCamera(qlabs)
    hcamera.spawn()
    qcar.possess()

    QLabsRealTime().start_real_time_model(rtmodels.QCAR)

    return qcar
