import sys
from pathlib import Path


def move_unmatched_labels(images_dir: Path, labels_dir: Path):
    """Move label files that don't have matching image files in the images directory."""
    # Ensure the duplicates directory exists
    duplicates_labels_dir = labels_dir / "duplicates"
    duplicates_labels_dir.mkdir(exist_ok=True)

    # Gather all image filenames in images_dir non-recursively
    image_files = {
        file.stem for file in images_dir.glob("*.png")
    }  # Adjust for .png extension

    # Process each label file in labels_dir non-recursively
    for label_file in labels_dir.glob("*.txt"):  # Assumes label files are .txt
        if label_file.stem not in image_files:
            # Move unmatched label files to the duplicates subdirectory
            new_path = duplicates_labels_dir / label_file.name
            label_file.rename(new_path)
            print(f"Moved {label_file} to {new_path}")


def main():
    if len(sys.argv) > 2:
        images_dir_path = Path(sys.argv[1])
        labels_dir_path = Path(sys.argv[2])
        if images_dir_path.exists() and labels_dir_path.exists():
            move_unmatched_labels(images_dir_path, labels_dir_path)
            print("Label file processing completed.")
        else:
            print("Invalid directory paths.")
    else:
        print("Please provide paths to the images and labels directories.")


if __name__ == "__main__":
    main()
