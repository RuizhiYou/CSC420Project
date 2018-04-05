import cv2
import os

SPEED = 24
# SPEED = 10

def combine_images(image_folder, saved_vedio):
    images = os.listdir(image_folder)
    print ("image_folder: {}".format(image_folder))
    if '.DS_Store' in images:
        images.remove('.DS_Store')
    print (images)
    print(image_folder)
    print(images[0])
    img = cv2.imread(os.path.join(image_folder,images[0]))
    height, width, layers = img.shape

    if os.path.exists(saved_vedio):
        print("remove the orignal saved file")
        os.remove(saved_vedio)

    video = cv2.VideoWriter(saved_vedio,-1,SPEED,(width,height))

    for i in range(len(images)):
        print ("processing image: {}...".format(images[i]))
        # img = cv2.imread(image_folder + str(i) + '.jpg')
        img = cv2.imread(os.path.join(image_folder,images[i]))
        video.write(img)


    cv2.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    combine_images('./final_images/', './saved_video/video.mp4')

