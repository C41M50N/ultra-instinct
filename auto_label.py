from pathlib import Path

from ultralytics import YOLO
from ultralytics.engine.results import Results

from enums import ObjectType


images_path = Path("dataset/images")
labels_path = Path("dataset/labels")
augs_path = Path("dataset/aug")
model_path = Path("yolov8n.pt")

model = YOLO(model_path)
img_paths = tuple(images_path.glob("*.png"))

for img_index, img in enumerate(img_paths):
    results: Results = model.predict(img, verbose=False)[0]
    boxes = results.boxes

    aug_save_path = augs_path / img.name
    results.save(aug_save_path)

    obj_strs: list[str] = []
    for i in range(len(boxes.cls)):
        xywhn_strs = [str(n) for n in boxes.xywhn[i].tolist()]
        obj_cls = str(ObjectType(int(boxes.cls[i])))
        obj_str = " ".join([obj_cls, *xywhn_strs])
        obj_str_w_newline = f"{obj_str}\n"
        obj_strs.append(obj_str_w_newline)
        print(f"{img_index}/{len(img_paths)}")

    label_path = labels_path / f"{img.stem}.txt"
    with open(label_path, "w") as f:
        f.writelines(obj_strs)
