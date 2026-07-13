import numpy
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

PIXEL_WIDTH = 10

def line_spacing(m):
    n = PIXEL_WIDTH # n = number of elements in array
    # m = number of lines in the array

    arr = [0] * n

    if m <= 0: # Return all zeros if there are no lines
        return arr
    elif m == 1: # Return a single 1 if there is only one line
        arr[PIXEL_WIDTH // 2] = 1
        return arr
    elif m >= n: # Return a full array if there are 10+ lines
        return [1] * 10
    else:
        # Scale indicies properly?
        for i in range(m):
            index = round(i / (m - 1) * (n - 1))
            arr[index] = 1
        return arr

# Convert to greyscale
img = Image.open('test-image.jpg').convert("L")
pixels = numpy.array(img)

commands = []
# "Simple" - draw a line for each pixel

# Store last x and y position so we know when we're on a diagonal and we shouldn't draw, and also for drawing multiple
# lines so we know where to start again
last_y = 0
last_x = 0
for row in range(len(pixels)):
    for column in range(len(pixels[0])):
        x = column * PIXEL_WIDTH
        y = row * PIXEL_WIDTH

        brightness = pixels[row][column]

        # Up to 1 line per pixel -
        number_of_lines = int((255 - brightness) // (255 / PIXEL_WIDTH))

        if number_of_lines and y == last_y:
            commands.append("PEN DOWN")
            line_arr = line_spacing(number_of_lines)
            for i in range(PIXEL_WIDTH):
                # If the line exists
                if line_arr[i]:
                    commands.append("PEN UP")
                    commands.append("MOVE " + str(last_x) + " " + str(y + i))
                    commands.append("PEN DOWN")
                    commands.append("MOVE " + str(x) + " " + str(y + i))

        # Lift the pen - high brightness value or it's a diagonal
        else:
            commands.append("PEN UP")

        last_y = y
        last_x = x


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