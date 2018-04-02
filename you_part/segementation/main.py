from inference import *
from shotDetection import *
import argparse

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

def main(images, output, modelName):

    segmentation(images, output, modelName)
    #findCutScene(output)

if __name__ == '__main__':
    args = get_arguments()
    folder = args.img_path
    images = os.listdir(folder)
    images = sorted(images, key=lambda x: (x.split('.')[0]))
    images = [os.path.join(folder, image) for image in images]
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    main(images, args.save_dir, args.model)