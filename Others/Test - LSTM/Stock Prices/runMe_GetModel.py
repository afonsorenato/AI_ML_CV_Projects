# Some tests on LSTM networks
# This test is using dataset of stocks for price prediction
# Renato Afonso

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model

# Import training set
dataset_train = pd.read_csv("Google_Stock_Price_Train.csv")
training_set = dataset_train.iloc[:, 1:2].values

# Feature scaling
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Create data structure
x_train = []
y_train = []

for i in range(60, 1258):
    x_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

# Reshaping
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# init the RNN
model = Sequential()

# Adding layers for the LSTM
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))

# Units is what is going out on the next layer
# Return seq true because info will pass to a further layer
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50))
model.add(Dropout(0.2))

# This is the output final layer: output is 1
model.add(Dense(units = 1))

# Compile the network
model.compile(optimizer='adam', loss='mean_squared_error')

# Fit to the RNN training set
model.fit(x_train, y_train, epochs=50, batch_size=32)

# Save the model
model.save("stocks_model.h5")
print("Model saved")

