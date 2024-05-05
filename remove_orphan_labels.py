from pathlib import Path
import os

images_dir = Path("dataset\\images")
labels_dir = Path("dataset\\labels")

image_names = {f.stem: f for f in images_dir.glob("*.png")}
label_names = {f.stem: f for f in labels_dir.glob("*.txt")}
label_names.pop("classes")


for label_name, label_path in label_names.items():
    if image_names.get(label_name, None) is None:
        print(label_path)
        os.remove(label_path)


None
