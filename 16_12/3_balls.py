import cv2
import time
import random

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

prev_time, curr_time = time.time(), time.time()
prev_x, prev_y, curr_x, curr_y = 0, 0, 0, 0

ball_colors = {
    "red": {"lower": (0, 150, 140), "upper": (15, 255, 255)},
    "green": {"lower": (51, 90, 120), "upper": (70, 255, 255)},
    "yellow": {"lower": (20, 80, 160), "upper": (35, 255, 255)}
}


def random_colors(colors):
    c = colors.copy()
    random.shuffle(c)
    return tuple(c)


def get_order_ball(green, yellow, red):
    colors = [(green[0][0], 'g'), (yellow[0][0], 'y'), (red[0][0], 'r')]
    colors.sort()
    return colors[0][1], colors[1][1], colors[2][1]


def detection_of_ball(bound):
    mask = cv2.inRange(hsv, ball_colors[bound]['lower'], ball_colors[bound]['upper'])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            return (curr_x, curr_y), radius

    return None


guessed_colors = random_colors(['g', 'y', 'r'])
print(guessed_colors)

while cam.isOpened():
    isVictory = False

    ret, image = cam.read()
    curr_time = time.time()
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    green_circle = detection_of_ball('green')
    yellow_circle = detection_of_ball('yellow')
    red_circle = detection_of_ball('red')

    balls = [green_circle, yellow_circle, red_circle]

    if balls[0] and balls[1] and balls[2]:
        ordered_colors = get_order_ball(green_circle, yellow_circle, red_circle)
        if ordered_colors == guessed_colors:
            isVictory = True

    if isVictory:
        print("Отгадал")

    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
