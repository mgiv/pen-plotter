import numpy
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import random

PIXEL_WIDTH = 10
MAX_LINES = int(255 // (255 / PIXEL_WIDTH))

# Convert to greyscale
img = Image.open('test-image.jpg').convert("L")
pixels = numpy.array(img)

commands = []

# Converts n into an index, where n < PIXEL_WIDTH, converting it so that it's reasonably equally spaced
# We could randomize it, but we would need to create a random lookup table

# Generate list of random numbers
num_table = list(range(PIXEL_WIDTH))
random.shuffle(num_table)

def t_num(n):
    if n >= PIXEL_WIDTH:
        return 0
    return num_table[n]

for row in range(len(pixels)):
    for darkness_level in range(MAX_LINES):
        # How big of a line to draw
        line_counter = 0
        for col in range(len(pixels[0])):
            # Get darkness value, based on inverted pixel brightness and also the width of the pixels
            darkness = int((255 - pixels[row][col]) // (255 / PIXEL_WIDTH))

            # If the darkness is >= the current value, add this pixel to the list to draw.
            if darkness > darkness_level:
                line_counter += 1

            at_end = (col == len(pixels[0]) - 1)
            # Either the next pixel is brighter than the current darkness value, or we're at the end of a line.
            # We need to draw the line now. We also need to make sure there is a line.
            if (darkness < darkness_level or at_end) and line_counter:
                # Move to start of line

                x = col * PIXEL_WIDTH

                # Add the last pixel onto the line
                if at_end and darkness >= darkness_level:
                    x += PIXEL_WIDTH

                start_x = x - line_counter * PIXEL_WIDTH

                y = row * PIXEL_WIDTH

                commands.append("PEN UP")
                commands.append(f"MOVE {start_x} {y + t_num(darkness_level)}")
                commands.append("PEN DOWN")
                commands.append(f"MOVE {x} {y + t_num(darkness_level)}")
                line_counter = 0

commands.append("PEN UP")

# Simulation
toolhead_pos = (0, 0)

lines = []

pen = "up"
for command_num in range(len(commands)):
    command = commands[command_num].split(" ")
    if command[0] == "MOVE":
        x = int(command[1])
        y = int(command[2])
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
    elif command[0] == "HOME":
        # Do nothing for now
        pass


# Matplotlib stuff copied from their examples page. Best to ignore for now
fig, ax = plt.subplots(figsize=(10, 12), dpi=300)
# set axes limits manually because Collections do not take part in autoscaling
ax.set_xlim(0, len(pixels[0]) * 10)
ax.set_ylim(0, len(pixels) * 10)
ax.invert_yaxis()
ax.set_aspect("equal")  # to make the arcs look circular
# create a LineCollection with the half-circles
# its properties can be set per line by passing a sequence (here used for *colors*)
# or they can be set for all lines by passing a scalar (here used for *linewidths*)
line_collection = LineCollection(lines, linewidths=0.3, colors="black")
ax.add_collection(line_collection)

plt.show()