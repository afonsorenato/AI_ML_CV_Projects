import tensorflow
import mrcnn.config
import mrcnn.model
import mrcnn.visualize

import os
import cv2

#https://blog.paperspace.com/mask-r-cnn-in-tensorflow-2-0/


class SimpleConfig(mrcnn.config.Config):
    NAME = "coco_inference"

    NUM_CLASSES = 2
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


model = mrcnn.model.MaskRCNN(mode="inference",
                             config=SimpleConfig(),
                             model_dir=os.getcwd())

model.load_weights(filepath="grocery_model.h5",
                   by_name=True)

images = [cv2.imread("grocery_img_1.jpg"),
          cv2.imread("grocery_img_2.jpg")]

for sample in images:
    r = model.detect(images=[sample], verbose=0)

    CLASS_NAMES = ['BG', 'tomato']
    r = r[0]

    mrcnn.visualize.display_instances(image=sample,
                                      boxes=r['rois'],
                                      masks=r['masks'],
                                      class_ids=r['class_ids'],
                                      class_names=CLASS_NAMES,
                                      scores=r['scores'])
