from pathlib import Path

from ultralytics import YOLO

model_path = Path("model.pt")
img_path = Path("aug_124.png")

model = YOLO(model_path)
results = model.predict(img_path)[0]
results.save("orig_aug_124.png")

None