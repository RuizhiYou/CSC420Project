from inference import *
from shotDetection import *

def main(images, output, modelName):

    segmentation(images, output, modelName)
    findCutScene(output)

if __name__ == '__main__':
    args = get_arguments()
    folder = args.img_path
    images = os.listdir(folder)
    images = [os.path.join(folder, image) for image in images]
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    main(images, args.save_dir, args.model)