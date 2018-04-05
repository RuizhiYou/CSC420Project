import cv2
import os
import itertools
import numpy as np
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from scipy import misc

THRESHOLD = 2
DFD_THRESHOLD = 4
DOWN_RATIO = 0.1

def calculateHistogram(image):
    img = cv2.imread(image)
    color = ('b','g','r')
    colorHistogram = []
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        colorHistogram.append(histr)

    return np.array(colorHistogram)

def dfd(previous, current, flow=None):
    # Normalize
    if np.sum(previous) != 0:  previous = previous / np.sum(previous)
    if np.sum(current) != 0:  current = current / np.sum(current)

    flow = cv2.calcOpticalFlowFarneback(
        previous, current, flow, 0.5, 3, 15, 3, 5, 1.1, 0)

    height, width = previous.shape
    reconstruct = np.empty(previous.shape)

    for x, y in itertools.product(range(width), range(height)):
        dy, dx = flow[y, x]
        rx = max(0, min(x + int(dx), width - 1))
        ry = max(0, min(y + int(dy), height - 1))
        reconstruct[y, x] = current[ry, rx]

    return np.mean(np.abs(previous - reconstruct))

# mode 0 for optical flow method. 1 for color histogram
def findCutScene(files, mode=0):
    cuts = []
    # Color Hitogram
    if (mode):
        for i in range(len(files)):
            filename = files[i]
            if (i == 0):
                image = filename
                prev = calculateHistogram(image)
                prevDiff = float('inf')
            else:
                cur = calculateHistogram(filename)
                diff = np.linalg.norm(cur - prev)
                if abs(diff - prevDiff) > THRESHOLD * prevDiff:
                    cuts.append(i)
                    print("BINGO")

                print(filename)
                print(diff)

                prev = cur
                prevDiff = diff
    # Optical Flow DFD
    else:
        for i in range(len(files)):
            filename = files[i]
            if (i == 0):
                prev = cv2.imread(filename)
                prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
                # Down-sampling increases efficienty
                prev = misc.imresize(prev, DOWN_RATIO)
                prevDistance = float('inf')
            else:
                cur = cv2.imread(filename)
                cur = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
                # Down-sampling increases efficienty
                cur = misc.imresize(cur, DOWN_RATIO)
                distance = dfd(prev, cur)
                ratio = distance / prevDistance
                if (ratio > DFD_THRESHOLD):
                    cuts.append(i)
                    print("BINGO")
                prev = cur
                prevDistance = distance

    return cuts

def plotCuts(cuts, files):
    cut = 1
    for i in range(len(files)):
        if (i in cuts): cut += 1

        imageFile = files[i]
        im1 = Image.open(imageFile)
        # Drawing the text on the picture
        draw = ImageDraw.Draw(im1)
        # HACK: Replace this with your own font
        font_path = "Hack-Bold.ttf"
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)
        draw.text((0, 0), "Scene{}".format(cut), (255, 255, 0), font=font)
        print(imageFile)
        _ = ImageDraw.Draw(im1)

        # Save the image with a new name
        im1.save(imageFile)

if __name__ == '__main__':
    directory = os.fsencode("./test")
    files = os.listdir(directory)
    files = [os.fsdecode(file) for file in files if os.fsdecode(file).split(".")[-1] == "jpg"]
    files = sorted(files, key=lambda x: (x.split('.')[0]))
    files = [os.path.join('./test', filename) for filename in files]
    cuts = findCutScene(files, mode=0)
    print(cuts)
