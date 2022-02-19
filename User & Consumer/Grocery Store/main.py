#https://towardsdatascience.com/mask-rcnn-implementation-on-a-custom-dataset-fd9a878123d4

import shutil
import sys
import os
import json
import datetime
import numpy as np
import skimage.draw
import cv2
import matplotlib.pyplot as plt

from mrcnn.visualize import display_instances
from mrcnn.config import Config
from mrcnn import model as modellib, utils

from CustomDataset import CustomDataset
from CustomConfig import CustomConfig
from grocery_lib import train

ROOT_DIR = os.path.abspath("wastedata-Mask_RCNN-multiple-classes/main/Mask_RCNN/")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library


# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

config = CustomConfig()
model = modellib.MaskRCNN(mode="training", config=config,
                                  model_dir=DEFAULT_LOGS_DIR)

weights_path = COCO_WEIGHTS_PATH
if not os.path.exists(weights_path):
  utils.download_trained_weights(weights_path)

model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])

train(model, config)