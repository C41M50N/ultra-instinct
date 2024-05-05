from PIL import Image
from pathlib import Path
import shutil

# Directory containing images
images_dir = Path(r"dataset\images")
backup_dir = Path(r"dataset\backup_images")
backup_dir.mkdir(exist_ok=True)

valid_pixels = [(0, 0, 0, 255), (0, 1, 0, 255)]

# Iterate over all .png images in the directory
for image_path in images_dir.glob("*.png"):
    # image_path = Path("dataset\\images\\4035.png")
    # shutil.copyfile(image_path, backup_dir / image_path.name)
    # Open the image
    with Image.open(image_path) as img:
        img = img.convert("RGBA")  # Ensure image is in RGBA format

        # Get the dimensions of the image
        width, height = img.size

        # Initialize cropping boundaries
        right_bound = width
        lower_bound = height

        if img.getpixel((width - 1, height - 1)) not in valid_pixels:
            continue

        # Find the first non-black pixel from the right
        for x in range(width - 1, -1, -1):
            column = img.crop((x, 0, x + 1, height))
            if any(column.getpixel((0, y)) not in valid_pixels for y in range(height)):
                right_bound = x + 1
                break

        # Find the first non-black pixel from the bottom
        for y in range(height - 1, -1, -1):
            row = img.crop((0, y, width, y + 1))
            if any(row.getpixel((x, 0)) not in valid_pixels for x in range(width)):
                lower_bound = y + 1
                break

        # Crop the image based on the detected boundaries
        cropped_img = img.crop((0, 0, right_bound, lower_bound))

        # Save the cropped image
        cropped_img.save(
            image_path
        )  # Overwrite the original image or specify a new path
