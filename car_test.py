
import os

from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.qcar import QLabsQCar
from qvl.real_time import QLabsRealTime

import pal.resources.rtmodels as rtmodels
from pal.products.qcar import IS_PHYSICAL_QCAR, QCarRealSense


CAMERA = QLabsQCar.CAMERA_RGB


def setup_car():
    os.system("cls")
    
    if IS_PHYSICAL_QCAR:
        camera = QCarRealSense("RGB", frameWidthRGB=640, frameHeightRGB=480)
        img = camera.read_RGB()
        print(img)
    else:
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
        # qcar.possess()

        QLabsRealTime().start_real_time_model(rtmodels.QCAR)

        return qcar


if __name__ == "__main__":
    setup_car()
