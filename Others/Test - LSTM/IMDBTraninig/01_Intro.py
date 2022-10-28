from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = Sequential()
model.add(Embedding(10000, 32))
model.add(SimpleRNN(32, return_sequences=True))
model.add(SimpleRNN(32, return_sequences=True))
model.add(SimpleRNN(32, return_sequences=True))
model.summary()