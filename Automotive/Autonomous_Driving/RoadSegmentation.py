import pandas as pd
import numpy as np
import os
import random
import tensorflow as tf
import cv2
import datetime

from tqdm import tqdm
from tensorflow import keras
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.models import Sequential, Model

from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Concatenate
from tensorflow.keras.layers import Input, Add, Conv2DTranspose
from tensorflow.keras.losses import SparseCategoricalCrossentropy, MeanSquaredError, BinaryCrossentropy
from tensorflow.keras.utils import plot_model
from tensorflow.keras import callbacks

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from IPython.display import clear_output

from IPython.display import HTML
from base64 import b64encode

IMG_SIZE = 128
N_CHANNELS = 3
N_CLASSES = 1
SEED = 123  # number used to initialize the random number generator

TRAINSET_SIZE = int(len(os.listdir(train_data_dir)) * 0.8)
print(f"Number of Training Examples: {TRAINSET_SIZE}")

VALIDSET_SIZE = int(len(os.listdir(train_data_dir)) * 0.1)
print(f"Number of Validation Examples: {VALIDSET_SIZE}")

TESTSET_SIZE = int(len(os.listdir(train_data_dir)) - TRAINSET_SIZE - VALIDSET_SIZE)
print(f"Number of Testing Examples: {TESTSET_SIZE}")

input_shape = (IMG_SIZE, IMG_SIZE, N_CHANNELS)

inputs = Input(input_shape)
vgg16_model = VGG16(include_top=False, weights='imagenet', input_tensor=inputs)

c1 = vgg16_model.get_layer("block3_pool").output
c2 = vgg16_model.get_layer("block4_pool").output
c3 = vgg16_model.get_layer("block5_pool").output

# Decoder
u1 = UpSampling2D((2, 2), interpolation='bilinear')(c3)
