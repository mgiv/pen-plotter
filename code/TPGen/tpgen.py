import time

import numpy
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import hilbert
import triangle
import serial
import svg

import edge_detection
import line_converter

def handle_image(filename, reduce_quality=False):
    # Convert to greyscale
    img = Image.open(filename).convert("L")
    # Resize to make the image small enough
    if reduce_quality:
        img.thumbnail((100, 100))
    else:
        img.thumbnail((1920, 1080))

    pixels = numpy.array(img)
    return pixels

def draw(lines, sizex, sizey):
    # Strange wizardry to show the colours in order of drawing
    custom_cmap = LinearSegmentedColormap.from_list("progress", ["#ffff00", "#444400", "#ff0000", "#440000", "#ff00ff", "#440044", "#00ffff", "#004444"])
    colors = [custom_cmap(i / max(1, len(lines) - 1)) for i in range(len(lines))]

    # Matplotlib stuff copied from their examples page. Best to ignore for now
    fig, ax = plt.subplots(figsize=(10, 12), dpi=300)
    # set axes limits manually because Collections do not take part in autoscaling
    ax.set_xlim(0, sizex)
    ax.set_ylim(0,  sizey)
    ax.set_aspect("equal")  # to make the arcs look circular
    # create a LineCollection with the half-circles
    # its properties can be set per line by passing a sequence (here used for *colors*)
    # or they can be set for all lines by passing a scalar (here used for *linewidths*)
    line_collection = LineCollection(lines, linewidths=0.3, colors=colors)
    ax.add_collection(line_collection)

    plt.show()

# Simulation of what it might look like if it was drawn
def interpreter(commands):
    toolhead_pos = (0, 0)

    lines = []

    pen = "up"
    for command_num in range(len(commands)):
        command = commands[command_num].split(" ")
        if command[0] == "MOVE":
            x = 15000 - int(command[1])
            y = 15000 - int(command[2])
            if pen == "down":
                lines.append([toolhead_pos, (x, y)])

            # Move the toolhead anyway, even if we aren't drawing a line\\
            toolhead_pos = x, y

        elif command[0] == "PEN":
            if command[1] == "DOWN":
                pen = "down"
            elif command[1] == "UP":
                pen = "up"

            else:
                print("INVALID COMMAND: " + command)
        elif command[0] == "SPEED":
            pass


    return lines


def convert_image(filename, method, simulate=True):
    pixels = handle_image(filename, reduce_quality=True)

    y_size = len(pixels)
    x_size = len(pixels[0])

    x_size = len(pixels[0])
    y_size = len(pixels)

    sf = 15000 // x_size
    # Conver the image into a series of lines with the number depending on brightness
    if method == "lines":

        p_code = line_converter.line_convert(pixels, 10)
    # Do the same as above but first, use canny edge detection to filter out only the edges
    elif method == "edge_lines":
        pixels = handle_image(filename, reduce_quality=True)
        p_code = edge_detection.edge_lines(pixels)

    # Pure edge detection - takes the edges and turns that into lines that perfectly match the geometry
    # Much better looking images but harder to program
    elif method == "edge_pure":
        pixels = handle_image(filename, reduce_quality=False)
        p_code = edge_detection.pure_edge(pixels)

    else:
        print("Unknown method")
        return None
    return p_code


if __name__ == "__main__":
    # Image conversion - lines, edges then lines or pure edges
    # p_code = convert_image(f"test-images/4.jpg", "edge_pure", True)

    # Hilbert curve (level, width)
    #p_code = hilbert.hilbert(7, 15000)
    # Sierpinski triangle (level, width)
    #p_code = triangle.triangle(5, 15000)
    # Load SVG (filename, width)
    p_code = svg.draw_svg("test-images/sticker.svg", 15000, 5000, 1500)
    do_draw = True
    p_code.insert(0, "SPEED 5000")
    p_code.append("PEN UP")
    p_code.append("MOVE 0 0")
    if do_draw:
        print(len(p_code))
        lines = interpreter(p_code)
        draw(lines, 15000, 15000)
    p_code.append("MOVE 15000 16000")

    input("Ready to draw. Press any key to continue")

    start = 0
    with serial.Serial("COM9", 115200, timeout=None) as ser:
        pen = "up"

        print("Sending RST to device")
        ser.write("RST\n".encode("utf-8"))


        for instruction in range(start, len(p_code)):

            # Wait until an instruction is requested
            print("Waiting for instruction")
            while True:
                cmd = ser.readline().decode("utf-8")
                print(f"Received: {cmd}")
                if "NEXT" in cmd:
                    break
                elif "STOP" in cmd:
                    exit(1)

            inst = p_code[instruction]
            if inst == "PEN UP":
                pen = "up"
            elif inst == "PEN DOWN":
                pen = "down"
            print(f"Sending instruction: {inst} ({instruction})")
            ser.write((inst + "\n").encode("utf-8"))
