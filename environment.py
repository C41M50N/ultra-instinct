import math
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
        location=[24.328, 18.0, 0.0],
        rotation=[0.0, 0.0, -1.6],
        waitForConfirmation=False,
    )

    stopsign2 = QLabsStopSign(qlabs)
    stopsign2.spawn(
        location=[24.328, 2.5, 0.0],
        rotation=[0.0, 0.0, -1.6],
        waitForConfirmation=False,
    )

    stopsign3 = QLabsStopSign(qlabs)
    stopsign3.spawn(
        location=[-10.719, 46.669, 0.185],
        rotation=[0.0, 0.0, 0.0],
        waitForConfirmation=False,
    )

    stopsign4 = QLabsStopSign(qlabs)
    stopsign4.spawn(
        location=[2.482, 46.673, 0.189],
        rotation=[0.0, 0.0, 0.0],
        waitForConfirmation=False,
    )

    # spawn traffic lights
    trafficlight1 = QLabsTrafficLight(qlabs)
    trafficlight1.spawn(location=[1.108, -12.534, 0.2], rotation=[0.0, 0.0, -1.6])

    trafficlight2 = QLabsTrafficLight(qlabs)
    trafficlight2.spawn(location=[-21.586, 14.403, 0.192], rotation=[0.0, 0.0, math.pi])

    trafficlight3 = QLabsTrafficLight(qlabs)
    trafficlight3.spawn(location=[-21.586, 33.136, 0.182], rotation=[0.0, 0.0, math.pi])

    trafficlight4 = QLabsTrafficLight(qlabs)
    trafficlight4.spawn(location=[24.271, 32.997, 0.18], rotation=[0.0, 0.0, 0.0])

    # Start spawn model

    # Change traffic light states every 3 seconds
    traffic_lights = [trafficlight1, trafficlight2, trafficlight3, trafficlight4]
    state_index = 0
    while True:
        state = [
            QLabsTrafficLight.STATE_RED,
            QLabsTrafficLight.STATE_YELLOW,
            QLabsTrafficLight.STATE_GREEN,
        ][state_index]
        for traffic_light in traffic_lights:
            traffic_light.set_state(state)
        state_index = (state_index + 1) % 3
        time.sleep(3)


# def terminate():
#     QLabsRealTime().terminate_real_time_model(rtmodels.QCAR_STUDIO)
