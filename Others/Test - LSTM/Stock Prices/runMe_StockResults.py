# Some tests on LSTM networks
# This script gets the model and runs it for prediction
# Renato Afonso

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
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

# Load test data
dataset_test = pd.read_csv("Google_Stock_Price_Test.csv")
real_stock_price = dataset_test.iloc[:, 1:2].values

# Import the model
model = load_model('stocks_model.h5')

# Get prediction
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis=0)
inputs = dataset_total[len(dataset_total) - len(dataset_test)-60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
x_test = []

for i in range(60,80):
    x_test.append(inputs[i-60:i, 0])


x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
predicted_stock_price = model.predict(x_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

print("Info going to be printed")
print("Results real: " + str(real_stock_price[0][0]))
print("Results predicted: " + str(predicted_stock_price[0][0]))

# Plot the data
"""
plt.plot(real_stock_price, color='red', label='Real stock price')
plt.plot(predicted_stock_price, color='blue', label="Predicted Stock price")
plt.title("Google Stock Price Prediction")
plt.xlabel("Time")
plt.ylabel("Google Stock price")
plt.legend()
plt.show()
"""



