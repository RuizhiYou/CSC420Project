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

if os.path.exists(saved_video_path):
    print ("remove the orignal saved file")
    os.remove(saved_video_path)

video = cv2.VideoWriter(saved_video_path,-1,2,(width,height))

for i in range(len(images)):
    print ("processing image: {}...".format(images[i]))
    # img = cv2.imread(image_folder + str(i) + '.jpg')
    img = cv2.imread(image_folder + images[i])
    video.write(img)


cv2.destroyAllWindows()
video.release()




