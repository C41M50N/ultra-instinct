import os
import time

from qvl.qlabs import QuanserInteractiveLabs
from qvl.real_time import QLabsRealTime
from qvl.stop_sign import QLabsStopSign
from qvl.traffic_light import QLabsTrafficLight


def main():
    # connect to Qlabs
    os.system("cls")
    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()

    # Spawn stop signs
    stopsign1 = QLabsStopSign(qlabs)
    stopsign1.spawn(
        location=[0.556, -12.568, 0.186],
        rotation=[0.0, 0.0, -9.5],  # [0.0, 0.0, -9.5]
        waitForConfirmation=False,
    )

    stopsign2 = QLabsStopSign(qlabs)
    stopsign2.spawn(
        location=[23.653, 28.756, 0.005],
        rotation=[0.0, 0.0, -15.1],
        waitForConfirmation=False,
    )

    x_offset = 24.222
    y_offset = 9.945
    z_offset = 0.2

    TrafficLight0 = QLabsTrafficLight(qlabs)
    TrafficLight0.spawn_degrees(
        [x_offset, y_offset, z_offset],
        [0, 0, 0],
        scale=[1, 1, 1],
        configuration=0,
        waitForConfirmation=True,
    )
    TrafficLight0.set_state(QLabsTrafficLight.STATE_GREEN)
    TrafficLight1 = QLabsTrafficLight(qlabs)
    TrafficLight1.spawn_degrees(
        [-21.586, 14.403, 0.192],
        [0, 0, 180],
        scale=[1, 1, 1],
        configuration=0,
        waitForConfirmation=True,
    )
    TrafficLight1.set_state(QLabsTrafficLight.STATE_RED)

    i = 0
    while True:
        i += 1
        # print(i)

        if i % 2 == 0:
            TrafficLight0.set_state(QLabsTrafficLight.STATE_GREEN)
            TrafficLight1.set_state(QLabsTrafficLight.STATE_RED)
        else:
            TrafficLight1.set_state(QLabsTrafficLight.STATE_GREEN)
            TrafficLight0.set_state(QLabsTrafficLight.STATE_RED)

        time.sleep(10)


# def terminate():
#     QLabsRealTime().terminate_real_time_model(rtmodels.QCAR_STUDIO)
