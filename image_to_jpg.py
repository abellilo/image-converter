import os
from PIL import Image

# ==========================================
# HEIC / HEIF SUPPORT
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
OUTPUT_FOLDER = "output_jpg"

# JPG quality: 1-100
JPG_QUALITY = 95


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

def convert_to_jpg(input_path, output_path):

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
        # HANDLE TRANSPARENCY
        # --------------------------------------
        #
        # JPG does not support transparency.
        #
        # Transparent areas are converted to
        # white before saving as JPG.
        #

        if image.mode in ("RGBA", "LA"):

            background = Image.new(
                "RGB",
                image.size,
                (255, 255, 255)
            )

            alpha = image.getchannel("A")

            background.paste(
                image.convert("RGB"),
                mask=alpha
            )

            converted_image = background

        elif image.mode == "P":

            # Paletted images may contain transparency
            if "transparency" in image.info:

                rgba_image = image.convert("RGBA")

                background = Image.new(
                    "RGB",
                    rgba_image.size,
                    (255, 255, 255)
                )

                alpha = rgba_image.getchannel("A")

                background.paste(
                    rgba_image.convert("RGB"),
                    mask=alpha
                )

                converted_image = background

            else:

                converted_image = image.convert("RGB")

        else:

            converted_image = image.convert("RGB")

        # --------------------------------------
        # SAVE AS JPG
        # --------------------------------------

        converted_image.save(
            output_path,
            "JPEG",
            quality=JPG_QUALITY,
            optimize=True,
            progressive=True
        )

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
    print("              JPG IMAGE CONVERTER")
    print("=" * 60)
    print()

    print(f"Input folder : {INPUT_FOLDER}/")
    print(f"Output folder: {OUTPUT_FOLDER}/")
    print(f"JPG quality  : {JPG_QUALITY}")
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

        # Create JPG filename
        output_filename = (
            filename_without_extension + ".jpg"
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

            convert_to_jpg(
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
        f"Your JPG images are in: {OUTPUT_FOLDER}/"
    )

    print()


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()