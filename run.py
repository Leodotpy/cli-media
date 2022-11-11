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


# get image input (argument after run.py in command)
if len(sys.argv) > 1:
    media_file = sys.argv[1]
else:
    media_file = input("Enter full input file directory: ")

# setup cv2 vidcap with input video file
vidcap = cv2.VideoCapture(media_file)
success, image = vidcap.read()

# loop through each frame
count = 0
while success:
    success, frame = vidcap.read()

    numpydata = np.asarray(frame)

    max_size = int(min(os.get_terminal_size())/1.1) # get min terminal with slight downscale
    cmd = ""

    mode = "halfwidth"

    # skip this many pixels in frame array at a time
    skip = math.floor(max((len(numpydata)/max_size), len(numpydata[0]))/max_size)

# mode halfwidth
    sys.stdout.write('\33[0m\n')
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

    cmd += '\33[0m\n'
    os.system(
        clear
    )
    sys.stdout.write(cmd)
    time.sleep(0.03)
    # clear terminal for new frame, "clear" is used for linux and "cls" for windows

    count += 1
