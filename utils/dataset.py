import shutil
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Sample:
    img_path: Path
    label_path: Path


val_percent = 0.1

images_path = Path("images")
labels_path = images_path / "out"

dataset_path = Path("dataset")

train_path = dataset_path / "train"
train_images_path = train_path / "images"
train_labels_path = train_path / "labels"

val_path = dataset_path / "val"
val_images_path = val_path / "images"
val_labels_path = val_path / "labels"

image_paths = {img_path.stem: img_path for img_path in images_path.glob("*.png")}
image_labels_paths = [
    Sample(image_paths[l.stem], l)
    for l in labels_path.glob("*.txt")
    if l.stem != "classes"
]

val_start_index = len(image_labels_paths) - len(image_labels_paths) * val_percent

for i, image_label in enumerate(image_labels_paths):
    if i < val_start_index:
        dest_images_path = train_images_path
        dest_labels_path = train_labels_path
    else:
        dest_images_path = val_images_path
        dest_labels_path = val_labels_path

    shutil.copyfile(image_label.img_path, dest_images_path / image_label.img_path.name)
    shutil.copyfile(
        image_label.label_path, dest_labels_path / image_label.label_path.name
    )

None
