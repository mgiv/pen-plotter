import cv2
import line_converter

# Code from https://learnopencv.com/edge-detection-using-opencv/
# Converts a cv2 image into another cv2 image, but with edge detection
def edge_detect(img):
    # Blur image to reduce noise I guess
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)

    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)  # Combined X and Y Sobel Edge Detection

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=100)  # Canny Edge Detection

    return edges

# Wrapper that converts to lines
def edge_lines(img):
    return list(line_converter.line_convert(cv2.bitwise_not(edge_detect(img)), pw=10))

# Converts an image into real lines
def pure_edge(img):
    edges = edge_detect(img)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    commands = []
    current_pos = (0, 0)
    r_contours = contours[::-1]
    for c in r_contours:

        perimeter = cv2.arcLength(c, True)
        if perimeter < 20:
            continue
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(c, epsilon, True)

        if len(approx) <= 2:
            continue

        mult = 15000 // len(img)

        commands.append("PEN UP")
        # Fast while travelling (and no, pycharm, travelling is not spelt with one l)
        commands.append("SPEED 5000")
        commands.append("MOVE " + str(approx[0][0][0] * mult) + " " + str(approx[0][0][1] * mult))
        commands.append("PEN DOWN")
        # Slower while drawing
        commands.append("SPEED 1000")
        for line in approx[1:]:
            commands.append("MOVE " + str(line[0][0] * mult) + " " + str(line[0][1] * mult))
        commands.append("PEN UP")

    return commands