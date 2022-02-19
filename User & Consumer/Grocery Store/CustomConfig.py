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

class CustomConfig(Config):
    """Configuration for training on the dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "object"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2
    # Number of classes (including background)
    NUM_CLASSES = 1 + 3  # Background + (Tuna, Rice, Tomato)
    # Number of training steps per epoch
    STEPS_PER_EPOCH = 10
    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.8
