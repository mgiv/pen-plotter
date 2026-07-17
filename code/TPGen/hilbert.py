

commands = []
cur_pos = (0, 0)
n = 10
w = 15000

def hilbert(levels, width=15000):
    global n
    global w
    w = width
    n = int(width/(2**levels-1))
    commands.append("MOVE 0 0")
    commands.append("PEN DOWN")
    _hilbert(levels)
    commands.append("PEN UP")
    return commands

def move(direction):
    global commands
    global cur_pos
    x, y = cur_pos
    match direction:
        case "UP":
            # Flipped because 0 is at the top
            y -= n
        case "DOWN":
            y += n
        case "LEFT":
            x -= n
        case "RIGHT":
            x += n
    cur_pos = x, y
    commands.append("MOVE " + str(x) + " " + str(y))

# Code modified from https://www.compuphase.com/hilbert.htm
def _hilbert(level, direction="UP"):
    if level == 1:
        match direction:
            case "LEFT":
                move("RIGHT")
                move("DOWN")
                move("LEFT")
            case "RIGHT":
                move("LEFT")
                move("UP")
                move("RIGHT")
            case "UP":
                move("DOWN")
                move("RIGHT")
                move("UP")
            case "DOWN":
                move("UP")
                move("LEFT")
                move("DOWN")

    else:
        match direction:
            case "LEFT":
                _hilbert(level - 1, "UP")
                move("RIGHT")
                _hilbert(level - 1, "LEFT")
                move("DOWN")
                _hilbert(level - 1, "LEFT")
                move("LEFT")
                _hilbert(level - 1, "DOWN")
            case "RIGHT":
                _hilbert(level - 1, "DOWN")
                move("LEFT")
                _hilbert(level - 1, "RIGHT")
                move("UP")
                _hilbert(level - 1, "RIGHT")
                move("RIGHT")
                _hilbert(level - 1, "UP")
            case "UP":
                _hilbert(level - 1, "LEFT")
                move("DOWN")
                _hilbert(level - 1, "UP")
                move("RIGHT")
                _hilbert(level - 1, "UP")
                move("UP")
                _hilbert(level - 1, "RIGHT")
            case "DOWN":
                _hilbert(level - 1, "RIGHT")
                move("UP")
                _hilbert(level - 1, "DOWN")
                move("LEFT")
                _hilbert(level - 1, "DOWN")
                move("DOWN")
                _hilbert(level - 1, "LEFT")
