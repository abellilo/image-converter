import os
from PIL import Image, ImageFilter, ImageEnhance
from pillow_heif import register_heif_opener

register_heif_opener()

# ==========================================
# SETTINGS
# ==========================================

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# Final output size: 4:5
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1350

# WebP quality
WEBP_QUALITY = 10

# Amount of blur applied to background
BLUR_RADIUS = 35

# Slightly darken the blurred background
BACKGROUND_DARKNESS = 0.85


# ==========================================
# SUPPORTED IMAGE FORMATS
# ==========================================

SUPPORTED_FORMATS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
    ".webp",
    ".heic",
    ".heif"
)


# ==========================================
# CREATE FOLDERS
# ==========================================

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==========================================
# RESIZE IMAGE WITHOUT DISTORTION
# ==========================================

def resize_contain(image, max_width, max_height):
    """
    Resize an image proportionally so that the entire
    image fits inside the specified dimensions.

    Nothing is cropped.
    Nothing is stretched.
    """

    image_copy = image.copy()

    image_copy.thumbnail(
        (max_width, max_height),
        Image.Resampling.LANCZOS
    )

    return image_copy


# ==========================================
# CREATE BLURRED BACKGROUND
# ==========================================

def create_blurred_background(image, width, height):
    """
    Create a blurred background from the original image.

    The background is allowed to crop because it is only
    the background. The original image itself is never cropped.
    """

    background = image.copy()

    # Make the background large enough to completely
    # cover the 4:5 canvas.
    background_ratio = width / height
    image_ratio = background.width / background.height

    if image_ratio > background_ratio:
        # Image is wider than the canvas
        new_height = height
        new_width = int(new_height * image_ratio)
    else:
        # Image is taller than the canvas
        new_width = width
        new_height = int(new_width / image_ratio)

    background = background.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    # Crop ONLY the blurred background so it fills
    # the entire canvas.
    left = (background.width - width) // 2
    top = (background.height - height) // 2
    right = left + width
    bottom = top + height

    background = background.crop(
        (left, top, right, bottom)
    )

    # Apply blur
    background = background.filter(
        ImageFilter.GaussianBlur(BLUR_RADIUS)
    )

    # Slightly darken the background
    background = ImageEnhance.Brightness(
        background
    ).enhance(BACKGROUND_DARKNESS)

    return background


# ==========================================
# PROCESS ONE IMAGE
# ==========================================

def process_image(input_path, output_path):
    """
    Convert one image to WebP and 4:5.
    """

    with Image.open(input_path) as image:

        # Handle animated GIFs by using the first frame
        try:
            image.seek(0)
        except Exception:
            pass

        # Convert image to RGBA so transparency is supported
        image = image.convert("RGBA")

        # --------------------------------------
        # CREATE BLURRED BACKGROUND
        # --------------------------------------

        background = create_blurred_background(
            image,
            OUTPUT_WIDTH,
            OUTPUT_HEIGHT
        )

        # --------------------------------------
        # RESIZE ORIGINAL IMAGE
        # --------------------------------------

        original = resize_contain(
            image,
            OUTPUT_WIDTH,
            OUTPUT_HEIGHT
        )

        # --------------------------------------
        # CREATE FINAL CANVAS
        # --------------------------------------

        final_image = background.copy()

        # --------------------------------------
        # CENTER ORIGINAL IMAGE
        # --------------------------------------

        x = (OUTPUT_WIDTH - original.width) // 2
        y = (OUTPUT_HEIGHT - original.height) // 2

        # Paste using the image's alpha channel
        final_image.alpha_composite(
            original,
            (x, y)
        )

        # --------------------------------------
        # CONVERT TO RGB FOR WEBP
        # --------------------------------------

        final_image = final_image.convert("RGB")

        # --------------------------------------
        # SAVE AS WEBP
        # --------------------------------------

        final_image.save(
            output_path,
            "WEBP",
            quality=WEBP_QUALITY,
            method=6
        )


# ==========================================
# PROCESS ALL IMAGES
# ==========================================

def main():

    files = os.listdir(INPUT_FOLDER)

    image_files = [
        file for file in files
        if file.lower().endswith(SUPPORTED_FORMATS)
    ]

    if not image_files:
        print()
        print("No supported images found.")
        print(f"Put your images inside: {INPUT_FOLDER}/")
        print()
        return

    print()
    print("=" * 55)
    print("        IMAGE CONVERTER")
    print("=" * 55)
    print()
    print(f"Input folder : {INPUT_FOLDER}/")
    print(f"Output folder: {OUTPUT_FOLDER}/")
    print(f"Output size  : {OUTPUT_WIDTH} x {OUTPUT_HEIGHT}")
    print("Aspect ratio : 4:5")
    print("Format       : WebP")
    print()
    print("-" * 55)

    successful = 0
    failed = 0

    for filename in image_files:

        input_path = os.path.join(
            INPUT_FOLDER,
            filename
        )

        # Remove original extension
        filename_without_extension = os.path.splitext(
            filename
        )[0]

        # New WebP filename
        output_filename = (
            filename_without_extension + ".webp"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_filename
        )

        try:

            print(f"Processing: {filename} ...", end=" ")

            process_image(
                input_path,
                output_path
            )

            print("✓")
            successful += 1

        except Exception as error:

            print("✗")
            print(f"   Error: {error}")

            failed += 1

    print()
    print("=" * 55)
    print("                 COMPLETE")
    print("=" * 55)
    print()
    print(f"Successfully converted: {successful}")
    print(f"Failed:                 {failed}")
    print(f"Output folder:          {OUTPUT_FOLDER}/")
    print()


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()