from __future__ import print_function

import argparse
import os
import sys
import time
from PIL import Image
import tensorflow as tf
import numpy as np
from scipy import misc

from model import FCN8s, PSPNet50, ENet, ICNet

save_dir = './output/'
model_path = {'pspnet': './model/pspnet50.npy',
              'fcn': './model/fcn.npy',
              'enet': './model/cityscapes/enet.ckpt',
              'icnet': './model/cityscapes/icnet.npy'}
# python3 inference.py --img-path '1.jpg' --model 'fcn'

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

def main():
    args = get_arguments()

    folder = args.img_path
    images = os.listdir(folder)

    if '.DS_Store' in images:
        images.remove('.DS_Store')

    if args.model == 'pspnet':
        model = PSPNet50()
    elif args.model == 'fcn':
        model = FCN8s()
    elif args.model == 'enet':
        model = ENet()
    elif args.model == 'icnet':
        model = ICNet()
        
    # model.read_input(args.img_path)

    # Init tf Session
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    init = tf.global_variables_initializer()

    sess.run(init)

    print ("before model loaded")
    model.load(model_path[args.model], sess)
    print ("model loaded successfully")
    print ("the type of the model: {}".format(type(model)))


    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    for item in images:
        print ("processing image: {}...".format(item))
        model.read_input(folder + item)
        preds = model.forward(sess)
        p = args.save_dir + args.model + '_' + model.img_name, preds[0]
        misc.imsave(args.save_dir + args.model + '_' + model.img_name, preds[0])
    
if __name__ == '__main__':
    main()
