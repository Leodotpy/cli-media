# display images and video in your terminal using Truecolor

import os
import random
import sys
from PIL import Image
import numpy as np
import random
import math

import cv2
import time
import signal

# set correct console clear command


def getClearCMD():
    # for windows
    if os.name == "nt":
        return "cls"

    # for mac and linux(here, os.name is 'posix')
    else:
        return "clear"


clear = getClearCMD()

# handler for if ctrl+c is pressed to exit loop


def handler(signum, frame):
    print("\n")
    quit()


# set handler
signal.signal(signal.SIGINT, handler)

# convert frame/image array into trucolor text output
def getCliFrame(numpydata, skip):
    cmd = ""
    for y in numpydata[::int(skip)]:
        hasAlpha = False
        l = ''
        for x in y[::int(skip/2)]:
            if len(x) > 3 and x[3] == 0:  # if alpha 0
                l += "\33[0m "

            else:
                l += f"\33[48;2;{x[2]};{x[1]};{x[0]}m "
                hasAlpha = True

        if hasAlpha:
            cmd += l + '\33[0m\n'

    # return cli output and size
    return cmd + '\33[0m\n', (len(numpydata[::int(skip)]), len(y[::int(skip/2)]))

# print media to terminal
def printMedia(cmd, size, debug=True):
    if debug:
        cmd = cmd  + f"output size: {size[0]}x{size[1]}" + '\n'

    os.system(
        clear
    )
    sys.stdout.write(cmd)


# get image input (argument after run.py in command)
if len(sys.argv) > 1:
    media_file = sys.argv[1]
else:
    media_file = input("Enter full input file directory: ")

# setup cv2 vidcap with input video file
vidcap = cv2.VideoCapture(media_file)
success, vid_frame = vidcap.read()

# setup cv2 imread with input image file
img_frame = cv2.imread(media_file)

# determine if mediafile is video or image
# if detect vid file
if img_frame is None and vid_frame is not None:
    is_vid = True
# elif detect image file
elif vid_frame is not None and img_frame is not None:
    is_vid = False
else:
    print("Error with inputfile. Type not valid.")
    quit()

# display image if input is image
if not is_vid:

    numpydata = np.asarray(img_frame)

    # get min terminal with slight downscale
    max_size = int(min(os.get_terminal_size())/1.2)

    mode = "halfwidth"

    # skip this many pixels in frame array at a time
    skip = math.floor(max((len(numpydata)/max_size),
                      len(numpydata[0]))/max_size)

    cmd, s = getCliFrame(numpydata, skip)

    printMedia(cmd, s)

    quit()

# loop through each frame
count = 0
while success:
    success, frame = vidcap.read()

    numpydata = np.asarray(frame)

    # get min terminal with slight downscale
    max_size = int(min(os.get_terminal_size())/1.2)

    mode = "halfwidth"

    # skip this many pixels in frame array at a time
    skip = math.floor(max((len(numpydata)/max_size),
                      len(numpydata[0]))/max_size)

# mode halfwidth
    sys.stdout.write('\33[0m\n')

    cmd, s = getCliFrame(numpydata, skip)

    printMedia(cmd, s)
    time.sleep(0.03)
    # clear terminal for new frame, "clear" is used for linux and "cls" for windows

    count += 1
