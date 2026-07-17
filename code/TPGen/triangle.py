import turtle

current_pos = (0, 0)

# Code modified from https://runestone.academy/ns/books/published/pythonds/Recursion/pythondsSierpinskiTriangle.html
def drawTriangle(points, commands):
    global current_pos

    # Different position, we need to lift
    commands.append("PEN UP")
    commands.append(f"MOVE {points[0][0]} {points[0][1]}")
    commands.append("PEN DOWN")
    commands.append(f"MOVE {points[1][0]} {points[1][1]}")
    commands.append(f"MOVE {points[2][0]} {points[2][1]}")
    commands.append(f"MOVE {points[0][0]} {points[0][1]}")
    current_pos = (points[0][0], points[0][1])

def getMid(p1,p2):
    return round((p1[0] + p2[0]) / 2), round((p1[1] + p2[1]) / 2)

def sierpinski(points, degree, commands):

    drawTriangle(points, commands)
    if degree > 0:
        sierpinski([points[0],
                        getMid(points[0], points[1]),
                        getMid(points[0], points[2])],
                   degree - 1, commands)
        sierpinski([points[1],
                        getMid(points[0], points[1]),
                        getMid(points[1], points[2])],
                   degree - 1, commands)
        sierpinski([points[2],
                        getMid(points[2], points[1]),
                        getMid(points[0], points[2])],
                   degree - 1, commands)

def triangle(depth):
    commands = ["PEN DOWN"]
    points = [[0, 0],[7400, 14800],[14800, 0]]
    sierpinski(points,depth, commands)
    return commands