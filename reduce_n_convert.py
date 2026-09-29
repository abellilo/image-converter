import os
from PIL import Image

# ==========================================
# SETTINGS
# ==========================================

INPUT_FOLDER = "input_webp"
OUTPUT_FOLDER = "output_webp"

# WebP quality
WEBP_QUALITY = 10


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
# HELPER: FORMAT FILE SIZE
# ==========================================

def format_size(size_in_bytes):
    """Formats bytes into human-readable units (KB/MB)."""
    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    return f"{size_in_bytes / (1024 * 1024):.2f} MB"


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

        if image.mode in ("RGBA", "LA"):
            converted_image = image.convert("RGBA")

        elif image.mode == "P":
            if "transparency" in image.info:
                converted_image = image.convert("RGBA")
            else:
                converted_image = image.convert("RGB")

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
    total_original_bytes = 0
    total_converted_bytes = 0

    # --------------------------------------
    # PROCESS EACH IMAGE
    # --------------------------------------

    for filename in image_files:

        input_path = os.path.join(
            INPUT_FOLDER,
            filename
        )

        filename_without_extension = os.path.splitext(
            filename
        )[0]

        output_filename = (
            filename_without_extension + ".webp"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_filename
        )

        try:

            convert_to_webp(
                input_path,
                output_path
            )

            # Get file sizes
            orig_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)

            total_original_bytes += orig_size
            total_converted_bytes += new_size

            # Calculate reduction percentage
            if orig_size > 0:
                reduction = ((orig_size - new_size) / orig_size) * 100
            else:
                reduction = 0

            # Output conversion summary for this file
            orig_str = format_size(orig_size)
            new_str = format_size(new_size)

            if reduction >= 0:
                print(
                    f"✓ {filename}: {orig_str} -> {new_str} ({reduction:.1f}% smaller)"
                )
            else:
                # If WebP turned out larger than original
                print(
                    f"✓ {filename}: {orig_str} -> {new_str} (+{abs(reduction):.1f}% larger)"
                )

            successful += 1

        except Exception as error:

            print(
                f"✗ {filename} -> Error: {error}"
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

    # Print overall savings summary
    if successful > 0 and total_original_bytes > 0:
        total_saved_bytes = total_original_bytes - total_converted_bytes
        total_reduction = (total_saved_bytes / total_original_bytes) * 100

        print(
            f"Original total size:   {format_size(total_original_bytes)}"
        )
        print(
            f"New WebP total size:   {format_size(total_converted_bytes)}"
        )
        print(
            f"Total space saved:     {format_size(total_saved_bytes)} ({total_reduction:.1f}% reduction)"
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