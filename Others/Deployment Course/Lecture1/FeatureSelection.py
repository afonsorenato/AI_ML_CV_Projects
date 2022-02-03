import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel

pd.pandas.set_option('display.max_columns', None)

x_train = pd.read_csv('train.csv')
x_test = pd.read_csv('test.csv')

sel_ = SelectFromModel(Lasso(alpha=0.001, random_state=0))

sel_.fit(x_train, y_train)
