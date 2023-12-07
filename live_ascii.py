import cv2 as cv
import os

os.system("color 0a")

def map_value(n, start1, stop1, start2, stop2):
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2


contrast = 10
SHADES = "Ñ@#W$9876543210?!abc;:+=-,._ " + " " * contrast
SHADES = str.join("", reversed(SHADES))

# Console codes
LINE_UP = "\033[1A"
LINE_CLEAR = "\033[K"

cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("error opening camera")
    exit()

clear_string = ""

while True:
    ret, frame = cam.read()
    if not ret:
        print("error in retrieving frame")
        break

    img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    img = cv.flip(img, 1)
    input_height, input_width = img.shape
    output_width, output_height = 150, int(150 * (input_height / input_width))
    img = iter(cv.resize(img, (output_width, output_height)).tobytes())

    ascii_string = ""

    for h in range(output_height):
        for w in range(output_width):
            pix = next(img)
            mapped_gray = int(map_value(pix, 0, 255, 0, len(SHADES) - 1))
            ascii_string += SHADES[mapped_gray]
        ascii_string += "\n"

    if not clear_string:
        for i in range(output_height):
            clear_string += LINE_UP + LINE_CLEAR

    print(clear_string, flush=True, end="")
    print(ascii_string, end="", flush=True)

cam.release()
