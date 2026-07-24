from svgpathtools import parse_path
import xml.etree.ElementTree as ET
import re
from enum import Enum
import ctypes

class Command(Enum):
    MOVE = 1
    PEN_UP = 2
    PEN_DOWN = 3
    SPEED = 4

def draw_svg(filename, canvas_width, up_speed, down_speed):
    xml_unclean = open(filename).read()
    xml = re.sub("xmlns.*?\".*?\"", "", xml_unclean)
    root = ET.fromstring(xml)
    width = root.attrib["width"]
    height = root.attrib["height"]
    if width > height:
        scale = canvas_width / float(width)
    else:
        scale = canvas_width / float(height)

    group = root.find("g")
    path_xml = group.find("path")

    d = path_xml.get("d")

    path = parse_path(d)
    commands = [f"SPEED {down_speed}"]
    s_prev = 0
    e_prev = 0
    for l in range(len(path)):
        s = (path[l].start.real * scale, path[l].start.imag * scale)
        e = (path[l].end.real * scale, path[l].end.imag * scale)

        # It's a different line. The end point of the last jumps to a new startpoint
        if s != e_prev:
            commands.append("PEN UP")
            # Faster speed while moving
            commands.append(f"SPEED {up_speed}")

            # Move to new startpoint
            commands.append(f"MOVE {15000 - round(s[0])} {round(s[1])}")

            # Slower when drawing
            commands.append(f"SPEED {down_speed}")
            commands.append("PEN DOWN")

        commands.append(f"MOVE {15000 - round(e[0])} {round(e[1])}")

        s_prev = s
        e_prev = e

    return commands

