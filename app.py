import pyautogui
from pyautogui import *
import mouse
import time
from pathlib import Path
from os import *
import glob
from datetime import date
from PIL import ImageChops
import math
import operator
from functools import reduce
import winshell

print('Welcome to the ScreenshotMate, Your automatic Windows screenshot companion.\n')
time.sleep(2)

decision = input('Dou you need a tutorial? [y = yes, n = no]: ').lower()

while decision not in ["y", "n"]:
    decision = input(
        "\nDou you need a tutorial? [y = yes, n = no]: ").lower()
if decision == 'y':
    time.sleep(1)
    print('\n\nPath to Your incoming screenshots folder is Your desktop\n')
    time.sleep(3)
    print('After providing nessesary inputs mark with a mouse which region You would like to him to watch for changes')

basepath = winshell.desktop()

# takes parent dir name (subject name) and child dir name (current date) for convenience
name = input('\n\nFolder name: ')

print('\n\n\n~~~ Type "ctrl+c" to exit. ~~~')
date = date.today()

# global variable for bounding box and 'i' for proper iteration and image comparision, i = 1 to create first screenshot named '1'
global i
i = 1
global im

# open screenshot window
hotkey('win', 'shift', 's')

# waits for the LMB downclick
mouse.wait(button='left', target_types=('down'))

# assigns relative (0,0) coords of mouse
x0, y0 = mouse.get_position()

mouse.wait(button='left', target_types=('up'))

# assigns ending mouse coords to new variables
x1, y1 = mouse.get_position()


# inverts mouse coords if nessesary to allow all directions of the mouse
if (x1-x0) < 0:
    x0, x1 = x1, x0

if (y1-y0) < 0:
    y0, y1 = y1, y0


# checks if path exists and creates it if not otherwise finds latest file and updates i variable to append more screenshots
path = Path(f'{basepath}\\{name}\\{date}')
if path.exists() == False:
    path.mkdir(parents=True, exist_ok=True)
else:
    # returns path of all files in coded dir with .jpg extension
    dirlist = glob.glob(f'{basepath}\\{name}\\{date}\\*.jpg')

    # if dir exists but is empty assigns i = 1 back again
    try:
        # returns the path for latest file in dir
        latest_file = max(dirlist, key=os.path.getctime)

        # splits the path to list with '\' and takes last argument (name wiith .jpg extension) then splits it with '.' and takes first argument (just the name)
        latest_file_name = latest_file.split('\\')[-1].split('.')[0]
        i = int(latest_file_name) + 1
    except:
        i = 1

# initial buffer time for first screenshot to omit the green flash after taking screenshot manually
time.sleep(1)

im = pyautogui.screenshot(region=(x0, y0, x1-x0, y1-y0))
im.save(f'{basepath}\\{name}\\{date}\\{i}.jpg')


# screenshot and save function
def shotAndSave():
    global i
    global im
    time.sleep(2)
    im1 = pyautogui.screenshot(region=(x0, y0, x1-x0, y1-y0))

    def rmsdiffFunc(im, im1):
        # Calculate the root-mean-square difference between two images

        h = ImageChops.difference(im, im1).histogram()

        # calculate rms
        rmsdiff = math.sqrt(reduce(operator.add,
                                   map(lambda h, i: h*(i**2), h, range(256))
                                   ) / (float(im.size[0]) * im.size[1]))
        return rmsdiff

    # assigns the rmsdiff result (float) to variable
    rmsdiff = rmsdiffFunc(im, im1)

    # decides if the rmsdiif variable is big enough to make another screenshot
    if rmsdiff > 25:
        # checking latest file number each time before saving new screenshot
        dirlist = glob.glob(f'{basepath}\\{name}\\{date}\\*.jpg')
        latest_file = max(dirlist, key=os.path.getctime)
        latest_file_name = latest_file.split('\\')[-1].split('.')[0]
        i = int(latest_file_name) + 1
        im1.save(f'{basepath}\\{name}\\{date}\\{i}.jpg')
        im = im1


while True:
    shotAndSave()
