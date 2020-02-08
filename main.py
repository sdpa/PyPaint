import os
import pyautogui
import cv2
from random import randint
import math
import numpy as np

"""
This program goes into a infinite Loop !!! Need to stopped at user discretion. 
"""
def find_controls(template, source_image):
    source_image = cv2.imread(source_image, 0)  # Reads image in color
    template = cv2.imread(template, 0)
    w, h = template.shape[::-1]

    # apply template matching
    res = cv2.matchTemplate(source_image, template, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Calculate the center:
    center = (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2))
    return center

def edit_RGB_values (edit_colors,RGB_locations,okLocation,RGB):
    # print(RGB_locations[key]) #<--- this points to the insert locations
    pyautogui.moveTo(edit_colors)
    pyautogui.click()
    for eachColor in RGB_locations:
        pyautogui.moveTo(RGB_locations[eachColor])
        pyautogui.click(clicks=2)
        pyautogui.press('backspace')
        pyautogui.typewrite(str(RGB[eachColor]))
    pyautogui.moveTo(okLocation)
    pyautogui.click()

def get_RGB_from_Image(imgHei, imgWid):
    x = randint(0, imgWid-1)
    y = randint(0, imgHei-1)
    # pixel_b, pixel_g, pixel_r = image[row][column]
    RGB_from_image = {'red': mainImg.item(y,x,2), 'green':mainImg.item(y,x,1),'blue':mainImg.item(y,x,0)}
    return RGB_from_image, x, y

def drawlines(x1, y1):
    r = 10
    x1 = start_point[0] + x1
    y1 = start_point[1] + y1

    # Use parametric equations
    t_degree = randint(0,360)
    t_radians = math.radians(t_degree)
    x2 = x1 + r*(math.cos(t_radians))
    y2 = y1 + r*(math.sin(t_radians))
    pyautogui.moveTo(x1, y1)
    pyautogui.dragTo(x2, y2, button='left')

    stepsize = 2  # moves over 2 pixels
    miniRsum = 0
    while(miniRsum < r):
        x1 = x1 + stepsize*(math.cos(t_radians+(math.pi/2)))
        y1 = y1 + stepsize*(math.sin(t_radians+(math.pi/2)))
        x2 = x1 + r * (math.cos(t_radians))
        y2 = y1 + r * (math.sin(t_radians))
        miniRsum = miniRsum + stepsize
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, button='left')
    return 0

if __name__== "__main__":
    # Calibrate  #Height = img.shape[0] , Width = img.shape[1]
    mainImg = cv2.imread('landscape.jpg', cv2.IMREAD_COLOR)
    maxWidth = 500
    maxHeight = 500
    scaling_factors = np.arange(1, 0, -0.001).tolist()
    for i in scaling_factors:
        if mainImg.shape[1] > maxWidth or mainImg.shape[0] > maxHeight:
            mainImg = cv2.resize(mainImg, (0, 0), fx=i, fy=i)
        else:
            break;
    imageWidth = mainImg.shape[1]
    imageHeight = mainImg.shape[0]
    start_point = (54, 261)
    os.system("Start /max mspaint")
    edit_colors = find_controls('edit_color.png', 'homescreen.png')  # 64x126 | 1920x1080
    RGB_locations = {'red':find_controls('red.PNG', 'edit_colors_window.png'),
                     'green':find_controls('green.PNG', 'edit_colors_window.png'),
                     'blue':find_controls('blue.PNG', 'edit_colors_window.png')}
    ok_button = find_controls('ok.png', 'edit_colors_window.png')

    while True:
        RGBFromImage, randomX, randomY = get_RGB_from_Image(imageHeight, imageWidth)
        edit_RGB_values(edit_colors, RGB_locations, ok_button, RGBFromImage)
        drawlines(randomX, randomY)




