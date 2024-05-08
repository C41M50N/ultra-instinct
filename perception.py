import multiprocessing
import os
from pathlib import Path
import multiprocessing
import time

from ultralytics import YOLO
import cv2
from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.qcar import QLabsQCar
from qvl.real_time import QLabsRealTime
from PIL import Image
import torch

from helper_funcs import get_image, run_perception
import pal.resources.rtmodels as rtmodels


CAMERA = QLabsQCar.CAMERA_RGB
model_path = Path("model.pt")

device = "cuda" if torch.cuda.is_available() else "cpu"


def main(perception_queue: multiprocessing.Queue, image_queue: multiprocessing.Queue):
    car = setup_car()
    model = YOLO(model_path)
    # model.to(device)

    i = 0
    while True:
        image = get_image(car, CAMERA)
        bgr_image = image.copy()
        bgr_image[:, :, [0, 2]] = bgr_image[:, :, [2, 0]]
        img = Image.fromarray(bgr_image)
        img.save(f"imgs/orig_{i}.png")
        
        results = run_perception(model, image)
        aug_img = results.plot(
            img=image,  # Plotting on the original image
            conf=True,  # Display confidence score
            boxes=True,  # Draw bounding boxes
            labels=True,  # Display labels
            masks=False,  # Assuming no masks to plot
            probs=False,  # Show probabilities if desired
            line_width=2,  # Line width of bounding boxes
            font_size=None,  # Automatically scale font size
            pil=False,  # Return as a numpy array
        )
        results.save(f"imgs/aug_{i}.png")
        i += 1
        image_queue.put(aug_img)
        perception_queue.put(results)


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
