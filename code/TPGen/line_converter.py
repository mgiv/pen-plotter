import random

# Turns an image into a series of horizontal lines, with brighter pixels getting more lines


def line_convert(pixels, pw):
    commands = []

    max_lines = int(255 // (255 / pw))

    # Converts n into an index, where n < PIXEL_WIDTH, converting it so that it's reasonably equally spaced
    # We could randomize it, but we would need to create a random lookup table

    # Generate list of random numbers
    num_table = list(range(pw))
    random.shuffle(num_table)

    def t_num(n):
        if n >= pw:
            return 0
        return num_table[n]

    for row in range(len(pixels)):
        for darkness_level in range(max_lines):
            # How big of a line to draw
            line_counter = 0
            for col in range(len(pixels[0])):
                # Get darkness value, based on inverted pixel brightness and also the width of the pixels
                darkness = int((255 - pixels[row][col]) // (255 / pw))

                # If the darkness is >= the current value, add this pixel to the list to draw.
                if darkness > darkness_level:
                    line_counter += 1

                at_end = (col == len(pixels[0]) - 1)
                # Either the next pixel is brighter than the current darkness value, or we're at the end of a line.
                # We need to draw the line now. We also need to make sure there is a line.
                if (darkness < darkness_level or at_end) and line_counter:
                    # Move to start of line

                    x = col * pw

                    # Add the last pixel onto the line
                    if at_end and darkness >= darkness_level:
                        x += pw

                    start_x = x - line_counter * pw

                    y = row * pw

                    x_size = len(pixels[0])
                    y_size = len(pixels)
                    sf = 15000 // (x_size * pw)


                    commands.append("PEN UP")
                    commands.append(f"MOVE {start_x * sf} {(y + t_num(darkness_level)) * sf}")
                    commands.append("PEN DOWN")
                    commands.append(f"MOVE {x * sf} {(y + t_num(darkness_level)) * sf}")
                    line_counter = 0

    commands.append("PEN UP")
    return commands


