import cv2
import os, pafy, math, random
import numpy as np
import datetime as dt
import tensorflow as tf
import matplotlib.pyplot as plt

from collections import deque
from moviepy.editor import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model
from sklearn.model_selection import train_test_split


seed_constant = 27
np.random.seed(seed_constant)
random.seed(seed_constant)
tf.random.set_seed(seed_constant)