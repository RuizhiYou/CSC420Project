import cv2
 
def combine_img(src_path, colored_path, out_path):
    src1 = cv2.imread(src_path)
    src2 = cv2.imread(colored_path)

    alpha = 0.7
    beta = 1.0 - alpha
    cv2.addWeighted(src1, alpha, src2, beta, 0.0, src1);
    cv2.imwrite(out_path,src1)
