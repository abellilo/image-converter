import os
from PIL import Image

# ==========================================
# OPTIONAL HEIC / HEIF SUPPORT
# ==========================================

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True

except ImportError:
    HEIC_SUPPORTED = False


# ==========================================
# SETTINGS
# ==========================================

INPUT_FOLDER = "input_images"
OUTPUT_FOLDER = "output_png"


# ==========================================
# SUPPORTED IMAGE FORMATS
# ==========================================

SUPPORTED_FORMATS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
    ".heic",
    ".heif"
)


# ==========================================
# CREATE FOLDERS
# ==========================================

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==========================================
# CONVERT ONE IMAGE
# ==========================================

def convert_to_png(input_path, output_path):

    with Image.open(input_path) as image:

        # --------------------------------------
        # HANDLE ANIMATED IMAGES
        # --------------------------------------
        #
        # Only the first frame is converted.
        #
        try:
            image.seek(0)
        except Exception:
            pass

        # --------------------------------------
        # HANDLE IMAGE MODE
        # --------------------------------------

        # Images that already support transparency
        if image.mode in ("RGBA", "LA"):

            converted_image = image.convert("RGBA")

        # Paletted images
        elif image.mode == "P":

            # Preserve transparency if available
            if "transparency" in image.info:
                converted_image = image.convert("RGBA")

            else:
                converted_image = image.convert("RGB")

        # Grayscale images
        elif image.mode == "L":

            converted_image = image.convert("L")

        # Grayscale + alpha
        elif image.mode == "LA":

            converted_image = image.convert("RGBA")

        # Everything else
        else:

            converted_image = image.convert("RGB")

        # --------------------------------------
        # SAVE AS PNG
        # --------------------------------------

        converted_image.save(
            output_path,
            "PNG",
            optimize=True
        )

        # --------------------------------------
        # CLEAN UP
        # --------------------------------------

        converted_image.close()


# ==========================================
# PROCESS ALL IMAGES
# ==========================================

def main():

    # --------------------------------------
    # CHECK HEIC SUPPORT
    # --------------------------------------

    if not HEIC_SUPPORTED:

        print()
        print("WARNING: HEIC/HEIF support is not installed.")
        print()
        print("Install it with:")
        print()
        print("    pip install pillow-heif")
        print()

    # --------------------------------------
    # FIND IMAGE FILES
    # --------------------------------------

    files = os.listdir(INPUT_FOLDER)

    image_files = [
        file
        for file in files
        if file.lower().endswith(SUPPORTED_FORMATS)
    ]

    # --------------------------------------
    # CHECK IF FOLDER IS EMPTY
    # --------------------------------------

    if not image_files:

        print()
        print("No supported images found.")
        print()
        print(
            f"Put your images inside the '{INPUT_FOLDER}' folder."
        )
        print()

        return

    # --------------------------------------
    # START
    # --------------------------------------

    print()
    print("=" * 60)
    print("              PNG IMAGE CONVERTER")
    print("=" * 60)
    print()

    print(f"Input folder : {INPUT_FOLDER}/")
    print(f"Output folder: {OUTPUT_FOLDER}/")
    print(f"HEIC support : {'YES' if HEIC_SUPPORTED else 'NO'}")
    print()

    print("-" * 60)

    successful = 0
    failed = 0

    # --------------------------------------
    # PROCESS EACH IMAGE
    # --------------------------------------

    for filename in image_files:

        input_path = os.path.join(
            INPUT_FOLDER,
            filename
        )

        # Remove original extension
        filename_without_extension = os.path.splitext(
            filename
        )[0]

        # Create PNG filename
        output_filename = (
            filename_without_extension + ".png"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_filename
        )

        try:

            print(
                f"Converting: {filename} ...",
                end=" "
            )

            convert_to_png(
                input_path,
                output_path
            )

            print("✓")

            successful += 1

        except Exception as error:

            print("✗")

            print(
                f"    Error: {error}"
            )

            failed += 1

    # --------------------------------------
    # FINISHED
    # --------------------------------------

    print()

    print("=" * 60)
    print("                    COMPLETE")
    print("=" * 60)

    print()

    print(
        f"Successfully converted: {successful}"
    )

    print(
        f"Failed:                 {failed}"
    )

    print()

    print(
        f"Your PNG images are in: {OUTPUT_FOLDER}/"
    )

    print()


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()