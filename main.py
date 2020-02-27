import os
import pyautogui
import cv2
import random
import numpy as np
import math
from bresenham import bresenham
import os

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



def get_RGB_from_Image(point,img):
    x = point[0]
    y = point[1]
    # pixel_b, pixel_g, pixel_r = image[row][column]
    RGB_from_image = {'red': img.item(y,x,2), 'green':img.item(y,x,1),'blue':img.item(y,x,0)}
    return RGB_from_image, x, y

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

def drawlines(x1, y1):
    pixelsDrawn = []
    r = 10
    x1 = int(start_point[0] + x1)
    y1 = int(start_point[1] + y1)
    # Use parametric equations
    t_degree = random.randint(0,360)
    t_radians = math.radians(t_degree)
    x2 = x1 + int(r*(math.cos(t_radians)))
    y2 = y1 + int(r*(math.sin(t_radians)))
    pyautogui.moveTo(x1, y1)
    pyautogui.dragTo(x2, y2, button='left')
    pixelsDrawn = pixelsDrawn + (list(bresenham(x1, y1, x2, y2)))

    stepsize = 2  # moves over 2 pixels
    miniRsum = 0
    while(miniRsum < r):
        x1 = x1 + int(stepsize*(math.cos(t_radians+(math.pi/2))))
        y1 = y1 + int(stepsize*(math.sin(t_radians+(math.pi/2))))
        x2 = x1 + int(r * (math.cos(t_radians)))
        y2 = y1 + int(r * (math.sin(t_radians)))
        miniRsum = miniRsum + stepsize
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, button='left')
        pixelsDrawn = pixelsDrawn + (list(bresenham(x1, y1, x2, y2)))
    no_duplicate_list = []
    #Removes all duplicates in the list.
    for x in pixelsDrawn:
        if x not in no_duplicate_list:
            no_duplicate_list.append(x)
    #[no_duplicate_list.append(x) for x in pixelsDrawn if x not in no_duplicate_list]
    return no_duplicate_list

if __name__== "__main__":
    # Calibrate  #Height = img.shape[0] , Width = img.shape[1]
    mainImg = cv2.imread('landscape.jpg', cv2.IMREAD_COLOR)
    maxWidth = 800
    maxHeight = 600
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

    chooselist = [] #Creates a list of pixels from the image dimensions
    for i in range(0,imageWidth):
        for j in range(0,imageHeight):
            chooselist.append((i,j))
    #print("Array created: \n", chooselist)

    while(len(chooselist) > 0):
        randomPoint = random.choice(chooselist)
        RGBFromImage, randomX, randomY = get_RGB_from_Image(randomPoint,mainImg)
        edit_RGB_values(edit_colors, RGB_locations, ok_button, RGBFromImage)
        pixelsToDelete = drawlines(randomX, randomY)

        #Normalizes points back to image pixels.
        for i in range(len(pixelsToDelete)):
            #Performs tuple list substraction.
            pixelsToDelete[i] = tuple(np.subtract((pixelsToDelete[i][0],pixelsToDelete[i][1]),(54,261)))
        #This removes drawn pixels from the origial list.
        for pixel in pixelsToDelete:
            if(pixel in chooselist):
                chooselist.remove(pixel)


