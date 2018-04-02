import cv2
import numpy as np
import os

THRESHOLD = 3
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
            cur = calculateHistogram(os.path.join('./clip', filename))
            diff = np.linalg.norm(cur - prev)
            if (diff - prevDiff) > THRESHOLD * prevDiff:
                cuts.append(i)
                print("BINGO")

            print(filename)
            print(diff)

            prev = cur
            prevDiff = diff

    return cuts

if __name__ == '__main__':
    directory = os.fsencode("./clip")
    files = os.listdir(directory)
    files = [os.fsdecode(file) for file in files if os.fsdecode(file).split(".")[-1] == "jpg"]
    files = sorted(files, key=lambda x: (x.split('.')[0]))
    files = [os.path.join('./clip', filename) for filename in files]
    cuts = findCutScene(files)
    print(cuts)
