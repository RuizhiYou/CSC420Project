import cv2
import numpy as np
import os

def calculateHistogram(image):
    img = cv2.imread(image)
    color = ('b','g','r')
    colorHistogram = []
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        colorHistogram.append(histr)

    return np.array(colorHistogram)


directory = os.fsencode("./clip")
files = os.listdir(directory)
files = [os.fsdecode(file) for file in files]
files = sorted(files, key=lambda x: (x.split('.')[0]))
diff = []
for i in range(len(files)):
    filename = files[i]
    if (i == 0):
        image = os.path.join('./clip', filename)
        prev = calculateHistogram(image)
    else:
        cur = calculateHistogram(os.path.join('./clip', filename))
        diff.append(np.linalg.norm(cur - prev))
        prev = cur

print(np.argmax(diff))
print(max(diff))
print(diff)

