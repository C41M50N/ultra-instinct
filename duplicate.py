from concurrent.futures import ThreadPoolExecutor
import hashlib
import sys
import os
from pathlib import Path
from PIL import Image


def hash_image(image_path: Path):
    """Generate a SHA-256 hash for an image."""
    with Image.open(image_path) as img:
        # Convert image to bytes
        img_bytes = img.tobytes()
        # Create a hash object
        hash_obj = hashlib.sha256()
        # Update the hash object with the bytes of the image
        hash_obj.update(img_bytes)
        # Return the hex digest of the image
        return hash_obj.hexdigest()


def find_duplicates(directory: Path):
    """Identify duplicate images within the directory and return their paths grouped by hash."""
    hashes: dict[str, list[Path]] = {}

    # Filter image files across supported formats
    image_files = (
        list(directory.rglob("*.png"))
        + list(directory.rglob("*.jpg"))
        + list(directory.rglob("*.jpeg"))
    )

    # Process each file to compute its hash
    def process_file(file: Path):
        image_hash = hash_image(file)
        return file, image_hash

    with ThreadPoolExecutor() as executor:
        results = executor.map(process_file, image_files)

    for file, image_hash in results:
        if image_hash in hashes:
            hashes[image_hash].append(file)
        else:
            hashes[image_hash] = [file]

    # Filter out hashes that have only one file associated
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}


def move_duplicates(duplicates: dict[str, list[Path]], directory: Path):
    """Move duplicate files to a 'duplicates' folder, organizing by hash."""
    duplicates_folder = directory / "duplicates"
    duplicates_folder.mkdir(exist_ok=True)

    for image_hash, files in duplicates.items():
        hash_folder = duplicates_folder / image_hash
        hash_folder.mkdir(exist_ok=True)
        for file in files:
            new_path = hash_folder / file.name
            file.rename(new_path)
            print(f"Moved {file} to {new_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir_path = Path(sys.argv[1])
        if dir_path.exists():
            duplicates = find_duplicates(dir_path)
            if duplicates:
                print("Found duplicates, now moving them...")
                move_duplicates(duplicates, dir_path)
                print("Duplicates have been moved.")
            else:
                print("No duplicates found.")
        else:
            print("Invalid directory path.")
    else:
        print("Please provide a directory path.")
