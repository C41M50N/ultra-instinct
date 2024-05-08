from pathlib import Path

from ultralytics import YOLO


model_path = Path("models/best4.pt")
img_path = Path("crop171.png")

model = YOLO(model_path)
results = model.predict(img_path)[0]
results.save("aug_171.png")
