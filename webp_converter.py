import os
from PIL import Image

# ==========================================
# SETTINGS
# ==========================================

INPUT_FOLDER = "input_webp"
OUTPUT_FOLDER = "output_webp"

# WebP quality
WEBP_QUALITY = 90


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
    ".webp"
)


# ==========================================
# CREATE FOLDERS
# ==========================================

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==========================================
# CONVERT ONE IMAGE
# ==========================================

def convert_to_webp(input_path, output_path):

    with Image.open(input_path) as image:

        # Handle animated GIFs by using the first frame
        try:
            image.seek(0)
        except Exception:
            pass

        # --------------------------------------
        # HANDLE IMAGE MODE
        # --------------------------------------

        # Images with transparency
        if image.mode in ("RGBA", "LA"):
            converted_image = image.convert("RGBA")

        # Paletted images with transparency
        elif image.mode == "P":
            if "transparency" in image.info:
                converted_image = image.convert("RGBA")
            else:
                converted_image = image.convert("RGB")

        # Normal images
        else:
            converted_image = image.convert("RGB")

        # --------------------------------------
        # SAVE AS WEBP
        # --------------------------------------

        converted_image.save(
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
    print("              WEBP IMAGE CONVERTER")
    print("=" * 60)
    print()

    print(f"Input folder : {INPUT_FOLDER}/")
    print(f"Output folder: {OUTPUT_FOLDER}/")
    print(f"WebP quality : {WEBP_QUALITY}")
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

        # Create WebP filename
        output_filename = (
            filename_without_extension + ".webp"
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

            convert_to_webp(
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
        f"Your WebP images are in: {OUTPUT_FOLDER}/"
    )

    print()


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()