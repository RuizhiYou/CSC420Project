from __future__ import print_function

import argparse
import os
import sys
import time
from PIL import Image
import tensorflow as tf
import numpy as np
from scipy import misc
import shutil
from model import FCN8s, PSPNet50, ENet, ICNet
from color_image import *
from image_combined import *


save_dir = './output/'
model_path = {'pspnet': './model/pspnet50.npy',
              'fcn': './model/fcn.npy',
              'enet': './model/cityscapes/enet.ckpt',
              'icnet': './model/cityscapes/icnet.npy'}
# python3 inference.py --img-path '1.jpg' --model 'fcn'
colored_img_folder = './colored_img/'
saved_vedio = './saved_video/video.mp4'

def get_arguments():
    parser = argparse.ArgumentParser(description="Reproduced PSPNet")
    parser.add_argument("--img-path", type=str, default='',
                        help="Path to the RGB image file.",
                        required=True)
    parser.add_argument("--save-dir", type=str, default=save_dir,
                        help="Path to save output.")
    parser.add_argument("--model", type=str, default='',
                        help="pspnet or fcn",
                        choices=['pspnet', 'fcn', 'enet', 'icnet'],
                        required=True)

    return parser.parse_args()

def segmentation(images, output, modelName):

    if modelName == 'pspnet':
        model = PSPNet50()
    elif modelName == 'fcn':
        model = FCN8s()
    elif modelName == 'enet':
        model = ENet()
    elif modelName == 'icnet':
        model = ICNet()
        
    # model.read_input(args.img_path)

    # Init tf Session
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    init = tf.global_variables_initializer()

    sess.run(init)

    print ("before model loaded")
    model.load(model_path[modelName], sess)
    print ("model loaded successfully")
    print ("the type of the model: {}".format(type(model)))


    for item in images:
        print ("processing image: {}...".format(item))
        model.read_input(item)
        preds = model.forward(sess)
        p = output + modelName + '_' + model.img_name, preds[0]
        misc.imsave(os.path.join(output + (model.img_name)), preds[0])

def generate_vedio(colored_img_folder, saved_vedio, args):
    if os.path.exists(colored_img_folder):
        shutil.rmtree(colored_img_folder)
    os.makedirs(colored_img_folder)
    color_images(args.img_path, args.save_dir, colored_img_folder)
    combine_images(colored_img_folder, saved_vedio)

if __name__ == '__main__':
    args = get_arguments()
    folder = args.img_path
    images = os.listdir(folder)
    images = [os.path.join(folder, image) for image in images]
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    segmentation(images, args.save_dir, args.model)
    generate_vedio(colored_img_folder, saved_vedio, args)