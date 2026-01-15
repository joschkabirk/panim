import glob
import os

from PIL import Image, ImageDraw


def add_rounded_corners_gif(input_path, output_path, radius=20):
    """Add rounded corners to a GIF."""
    gif = Image.open(input_path)
    frames = []

    try:
        while True:
            frame = gif.copy().convert("RGBA")

            # Create rounded mask
            mask = Image.new("L", frame.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), frame.size], radius=radius, fill=255)

            # Apply mask
            frame.putalpha(mask)
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    # Save with transparency
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=gif.info.get("duration", 100),
        loop=gif.info.get("loop", 0),
        disposal=2,
    )


def add_rounded_corners_png(input_path, output_path, radius=20):
    """Add rounded corners to a PNG."""
    img = Image.open(input_path).convert("RGBA")

    # Create rounded mask
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)

    # Apply mask
    img.putalpha(mask)
    img.save(output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add rounded corners to GIFs and PNGs")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite original files instead of creating *_rounded versions",
    )
    args = parser.parse_args()

    if not args.overwrite:
        # Remove previous rounded files
        for pattern in ["assets/*_rounded.gif", "assets/*_rounded.png"]:
            for path in glob.glob(pattern):
                print(f"Removing previous file: {path}")
                try:
                    os.remove(path)
                except OSError as e:
                    print(f"Error removing file {path}: {e}")

    # Convert all GIFs in the assets folder
    for path in glob.glob("assets/*.gif"):
        if path.endswith("_rounded.gif"):
            continue
        if args.overwrite:
            temp_output = path.replace(".gif", "_temp.gif")
            add_rounded_corners_gif(path, temp_output, radius=20)
            os.replace(temp_output, path)
            print(f"Overwritten: {path}")
        else:
            output = path.replace(".gif", "_rounded.gif")
            add_rounded_corners_gif(path, output, radius=20)
            print(f"Converted: {path} -> {output}")

    # Convert all PNGs in the assets folder
    for path in glob.glob("assets/*.png"):
        if path.endswith("_rounded.png"):
            continue
        if args.overwrite:
            temp_output = path.replace(".png", "_temp.png")
            add_rounded_corners_png(path, temp_output, radius=20)
            os.replace(temp_output, path)
            print(f"Overwritten: {path}")
        else:
            output = path.replace(".png", "_rounded.png")
            add_rounded_corners_png(path, output, radius=20)
            print(f"Converted: {path} -> {output}")
