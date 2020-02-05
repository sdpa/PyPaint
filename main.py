import os
import time
import pyautogui
import cv2
import random

mainImg = cv2.imread('landscape.jpg',cv2.IMREAD_COLOR)
start_point = (32,238)
RGB_values = [0,0,0]
strokelength = 6
def start_mspaint():
    os.system("Start /max mspaint")
def close_mspaint():
    os.system("taskkill /f /im mspaint.exe")

#Find edit_colors center:
def find_edit_colors_location():
    img = cv2.imread('homescreen.png',0)
    edit_color_template = cv2.imread('edit_color.png',0)
    w, h = edit_color_template.shape[::-1]

    #apply template matching
    res = cv2.matchTemplate(img,edit_color_template,cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0]+ w, top_left[1] + h)

    #Calculate the center:
    center = (int((top_left[0]+bottom_right[0])/2) , int((top_left[1]+bottom_right[1])/2))
    return center

def find_RGB_boxes_with_cv2(edit_colors_location):
    pyautogui.moveTo(edit_colors_location)
    pyautogui.click()
    RGB_images = ['red.PNG','green.PNG','blue.PNG']
    RGB_locations = {'red': (), 'green': (), 'blue': ()}
    img = cv2.imread('edit_colors_window_template.png', 0)
    for i in range(len(RGB_images)):
        template = cv2.imread(RGB_images[i], 0)
        w, h = template.shape[::-1]
        # apply template matching
        res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # Calculate the center:
        insertLocation = (int((top_left[0] + bottom_right[0]) / 2) + 25, int((top_left[1] + bottom_right[1]) / 2))
        #insertLocation = (int(center[0] + (center[0])/2), center[1])
        RGB_locations[str(RGB_images[i])[:-4]] = (insertLocation)
    print(RGB_locations)
    print("Successful with CV2")
    return RGB_locations

def edit_RGB_values(RGB_locations):
    #print(RGB_locations[key]) #<--- this points to the insert locations
    #pyautogui.moveTo(RGB_locations[key])
    for eachColor in RGB_locations.values():
        pyautogui.moveTo(eachColor)
        pyautogui.click()
        pyautogui.press('backspace')
        pyautogui.typewrite('20')
    print("Successful edited all three colors")
def find_ok():
    location = pyautogui.locateOnScreen('ok.png')
    ok_center = pyautogui.center(location)
    return ok_center

def get_RGB_from_Image():
    x1 = random.randint(1,mainImg.shpape([0]))
    y1 = random.randint(1,mainImg.shape([1]))
    offsetLength = abs(random() * strokelength)
    x2 = x1 + random.randint(-offsetLength, offsetLength)
    y2 = y1 + random.randint(-offsetLength, offsetLength)
    RGB_from_image = {}
                                                #pixel_b, pixel_g, pixel_r = image[row][column]
    RGB_from_image['red'] = mainImg[x1,y1,2]
    RGB_from_image['green'] = mainImg[x1, y1, 1]
    RGB_from_image['blue'] = mainImg[x1, y1, 0]
    return RGB_from_image, x1, y1, x2, y2

if __name__== "__main__":
    #Initial setup
    start_mspaint()
    edit_colors_location = find_edit_colors_location()
    RGB_fields_location = find_RGB_boxes_with_cv2(edit_colors_location)
    #RGB_values_from_Img = get_RGB_from_Image()
    edit_RGB_values(RGB_fields_location)
    ok_location = find_ok()
    pyautogui.moveTo(ok_location)
    pyautogui.click()
    pyautogui.moveTo(edit_colors_location)
    pyautogui.click()
    #close_mspaint()
"""
    Top Left: Point(x=25, y=232)
    Bottom Right: Point(x = 1177, y = 880)
"""




