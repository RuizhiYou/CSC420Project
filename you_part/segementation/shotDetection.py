import cv2
import numpy as np
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

THRESHOLD = 2
def calculateHistogram(image):
    img = cv2.imread(image)
    color = ('b','g','r')
    colorHistogram = []
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        colorHistogram.append(histr)

    return np.array(colorHistogram)

def findCutScene(files):
    cuts = []
    for i in range(len(files)):
        filename = files[i]
        if (i == 0):
            image = filename
            prev = calculateHistogram(image)
            prevDiff = float('inf')
        else:
            cur = calculateHistogram(filename)
            diff = np.linalg.norm(cur - prev)
            if (diff - prevDiff) > THRESHOLD * prevDiff:
                cuts.append(i)
                print("BINGO")

            print(filename)
            print(diff)

            prev = cur
            prevDiff = diff

    return cuts

def plotCuts(cuts, files):
    cut = 1
    for i in range(len(files)):
        if (i in cuts): cut += 1

        imageFile = files[i]
        im1 = Image.open(imageFile)
        # Drawing the text on the picture
        draw = ImageDraw.Draw(im1)
        draw.text((0, 0), "Scene{}".format(cut), (255, 255, 0))
        print(imageFile)
        draw = ImageDraw.Draw(im1)

        # Save the image with a new name
        im1.save(imageFile)

if __name__ == '__main__':
    directory = os.fsencode("./clip")
    files = os.listdir(directory)
    files = [os.fsdecode(file) for file in files if os.fsdecode(file).split(".")[-1] == "jpg"]
    files = sorted(files, key=lambda x: (x.split('.')[0]))
    files = [os.path.join('./clip', filename) for filename in files]
    cuts = findCutScene(files)
    print(cuts)
