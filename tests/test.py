from pathlib import Path

from PIL import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results


def run_yolov8(model: YOLO, image_path: Path) -> Results:
    img = Image.open(image_path)
    return model(img)[0]


stop_path = Path("images/out0700.png")
greenlight_path = Path("images/out0276.png")
redlight_path = Path("images/out1039.png")

model = YOLO("model.pt")

stop_results = run_yolov8(model, stop_path)
greenlight_results = run_yolov8(model, greenlight_path)
redlight_results = run_yolov8(model, redlight_path)

stop_results.save("augmented_stop.png")
greenlight_results.save("augmented_greenlight.png")
redlight_results.save("augmented_redlight.png")
