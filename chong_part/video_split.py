import cv2
vidcap = cv2.VideoCapture('short_video.MOV')
success,image = vidcap.read()
count = 0
success = True

while success:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  # cv2.imwrite("./saved_images/%d.jpg" % count, image)     # save frame as JPEG file
  count += 1



