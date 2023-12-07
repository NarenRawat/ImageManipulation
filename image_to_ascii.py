import argparse
from io import BytesIO
from PIL import Image


def map_value(n, start1, stop1, start2, stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2


def rgb_to_greyscale(r, g, b):
    return int((0.299 * r) + (0.587 * g) + (0.114 * b))


parser = argparse.ArgumentParser(description="Converts image to ASCII art.")

parser.add_argument("image", help="Path of the image file.")
parser.add_argument(
    "--width",
    default=100,
    type=int,
    help="Width to which the image will be resized before converting. Should be in the range of 10 to 150. (Default=100)",
)
parser.add_argument(
    "--contrast",
    default=10,
    type=int,
    help="Contrast value in a range of 0 to 20. (Default=10)",
)
parser.add_argument(
    "--black-bg",
    action="store_true",
    help="Use if ASCII art is to be used in black background.",
)
parser.add_argument(
    "--output", help="If given, writes the ASCII art to the given file."
)
parser.add_argument(
    "--dev",
    action="store_true",
    help="Removes the range restriction from width and contrast.",
)

args = parser.parse_args()

if not args.dev:
    if args.contrast not in range(0, 21):
        parser.print_help()
        print()
        print("main.py: error: argument --contrast: not in range")
        exit(1)
    if args.width not in range(10, 151):
        parser.print_help()
        print()
        print("main.py: error: argument --width: not in range")
        exit(1)

try:
    img = Image.open(args.image)
    img_format = img.format
except Exception as e:
    print("Unable to open the image file.")
    exit(2)


SHADES = "Ñ@#W$9876543210?!abc;:+=-,._ " + " " * args.contrast

if args.black_bg:
    SHADES = str.join("", reversed(SHADES))


img_width = args.width
img_height = int((img.height / img.width) * img_width)

img = img.resize((img_width, img_height))
img = img.convert("RGBA")

if img_format != "PNG":
    png_image_buffer = BytesIO()
    img.save(png_image_buffer, "PNG", optimize=False)
    img.close()
    img = Image.open(png_image_buffer)

img_bytes = iter(img.tobytes())
img.close()
try:
    png_image_buffer.close()
except NameError as e:
    pass

ascii_art_string = ""


for h in range(img_height):
    for w in range(img_width):
        r = next(img_bytes)
        g = next(img_bytes)
        b = next(img_bytes)
        a = next(img_bytes)
        grey = rgb_to_greyscale(r, g, b)
        mapped_grey = int(map_value(grey, 0, 255, 0, len(SHADES)-1))
        ascii_art_string += SHADES[mapped_grey]
    ascii_art_string += "\n"


print(ascii_art_string)

if args.output:
    try:
        with open(args.output, "w") as file:
            file.write(ascii_art_string)

        print()
        print("File saved successfully.")
        print("Use monospaced font for viewing the ascii art, such as 'Courier'.")
    except Exception as e:
        print("Something went wrong while saving the ASCII art text file.")
        exit()
