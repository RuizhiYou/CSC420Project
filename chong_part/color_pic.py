import numpy as np
import cv2

source_img_path = './test_color/source/p1.png'
boundary_img_path = './test_color/source/p2.png'

source_img = cv2.imread(source_img_path)
boundary_img = cv2.imread(boundary_img_path)

print (source_img.shape)
print (boundary_img.shape)
gray_boundary_image = cv2.cvtColor(boundary_img, cv2.COLOR_BGR2GRAY)

if (source_img.shape == boundary_img.shape):
    for i in range(source_img.shape[0]):
        for j in range(source_img.shape[1]):
            print (gray_boundary_image[i,j])
            if (gray_boundary_image[i,j] > 4):
                m = 1
                # print ("AAA")
                source_img[i,j,1:] = gray_boundary_image[i,j]
            # else:
            #     print ("BBB")
                # source_img[i,j,:] = gray_boundary_image[i,j]
    cv2.imwrite('new_img.png',source_img)


else:
    print ("shape are different! Skip this pair!")