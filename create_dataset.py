import os
import shutil
from pathlib import Path
import random

# Set the seed for reproducibility
random.seed(42)

# Paths to the dataset directories
images_dir = Path("dataset/images")
labels_dir = Path("dataset/labels")

# Create directories for the training and validation splits
train_dir = Path("dataset/train")
val_dir = Path("dataset/val")

train_images_dir = Path("dataset/train/images")
train_labels_dir = Path("dataset/train/labels")

val_images_dir = Path("dataset/val/images")
val_labels_dir = Path("dataset/val/labels")

for d in [
    train_dir,
    val_dir,
    train_images_dir,
    train_labels_dir,
    val_images_dir,
    val_labels_dir,
]:
    os.makedirs(d, exist_ok=True)

# Get all image files; assuming image files are in formats like JPG, PNG, etc.
image_files = list(images_dir.glob("*.png"))

# Shuffle the list of image files to ensure random distribution
random.shuffle(image_files)

# Split ratio for training (80% training, 20% validation)
split_ratio = 0.8
split_index = int(len(image_files) * split_ratio)

# Split the images into training and validation sets
train_files = image_files[:split_index]
val_files = image_files[split_index:]


# Function to copy files to their new destination
def copy_files(files: list[Path], dest_images_dir: Path, dest_labels_dir: Path):
    for file in files:
        # Copy image
        shutil.copy(file, dest_images_dir / file.name)

        # Assuming label file has the same basename but with .xml extension
        label_file = labels_dir / f"{file.stem}.txt"
        if label_file.exists():
            shutil.copy(label_file, dest_labels_dir / label_file.name)


# Copy training files
copy_files(train_files, train_images_dir, train_labels_dir)

# Copy validation files
copy_files(val_files, val_images_dir, val_labels_dir)

print("Dataset splitting complete.")
