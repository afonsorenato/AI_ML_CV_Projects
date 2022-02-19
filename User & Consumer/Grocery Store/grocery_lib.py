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

def train(model, config):
    """Train the model."""
    # Training dataset.
    dataset_train = CustomDataset()
    dataset_train.load_custom("Dataset", "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = CustomDataset()
    dataset_val.load_custom("Dataset", "val")
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=10,
                layers='heads')