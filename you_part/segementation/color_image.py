import numpy as np
import cv2
import os

def color_image(source_img_path, boundary_img_path, saved_path, saved_name):

    source_img = cv2.imread(source_img_path)
    boundary_img = cv2.imread(boundary_img_path)

    if not os.path.exists(saved_path):
        os.makedirs(saved_path)

    if (source_img.shape == boundary_img.shape):
        for i in range(source_img.shape[0]):
            for j in range(source_img.shape[1]):
                    source_img[i,j,:] = 0.7 * source_img[i,j,:] + 0.3 * boundary_img[i,j,:]

        cv2.imwrite(os.path.join(saved_path, saved_name), source_img)

    else:
        print ("shape are different! Skip this pair!")

def combine_img(src_path, colored_path, saved_path, saved_name):
    src1 = cv2.imread(src_path)
    src2 = cv2.imread(colored_path)

    alpha = 0.7
    beta = 1.0 - alpha
    cv2.addWeighted(src1, alpha, src2, beta, 0.0, src1);
    cv2.imwrite(os.path.join(saved_path, saved_name), src1)

def color_images(source_folder, boundary_folder, saved_path):
    print (source_folder)
    print (boundary_folder)
    print (saved_path)
    source_images = os.listdir(source_folder)
    boundary_images = os.listdir(boundary_folder)

    if '.DS_Store' in source_images:
        source_images.remove('.DS_Store')
    if '.DS_Store' in boundary_images:
        boundary_images.remove('.DS_Store')
    for i in range(min(len(source_images), len(boundary_images))):
        print ('processing {} image...'.format(i))
        combine_img(os.path.join(source_folder,source_images[i]), os.path.join(boundary_folder,boundary_images[i]), saved_path, source_images[i])

