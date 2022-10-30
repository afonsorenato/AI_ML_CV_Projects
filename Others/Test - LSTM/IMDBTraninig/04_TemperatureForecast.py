import os
import numpy as np

from matplotlib import pyplot as plt

# Dataset
fname = "jena_climate_2009_2016.csv"

# Open file
f = open(fname)
data = f.read()
f.close()

lines = data.split('\n')
header = lines[0].split(',')
lines = lines[1:]

float_data = np.zeros((len(lines), len(header)-1))
for i, line in enumerate(lines):
    values = [float(x) for x in line.split(',')[1:]]
    float_data[i,:] = values

temp = float_data[:,1]
plt.plot(range(len(temp)), temp)
plt.show()


lookback = 720          # observations go back 5 days
steps = 6               # one data point per hour
delay = 144             # targets will be 24h in the future