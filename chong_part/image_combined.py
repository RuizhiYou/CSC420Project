import cv2
import os

image_folder = "./saved_images/"
images = os.listdir(image_folder)
saved_video_path = './saved_video/video.mp4'
if '.DS_Store' in images:
    images.remove('.DS_Store')
print (images)
img = cv2.imread(image_folder + images[0])
height , width , layers =  img.shape

video = cv2.VideoWriter(saved_video_path,-1,24,(width,height))

for i in range(len(images)):
    img = cv2.imread(image_folder + str(i) + '.jpg')
    video.write(img)

cv2.destroyAllWindows()
video.release()




