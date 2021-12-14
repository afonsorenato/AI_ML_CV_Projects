
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image


# Initialize the CNN
classifier = Sequential()
classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
classifier.add((Conv2D(32, (3, 3), activation='relu')))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add((Conv2D(16, (3, 3), activation='relu')))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add((Conv2D(8, (3, 3), activation='relu')))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten
classifier.add(Flatten())

# Fully connected
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=1, activation='sigmoid'))

# Compile the CNN
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# The dataset
train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

training_set = train_datagen.flow_from_directory('C:/Users/Renato/OneDrive/Ambiente de Trabalho/Datasets/training_set',
                                                 target_size=(64, 64),
                                                 batch_size=5,
                                                 class_mode='binary')

test_datagen = ImageDataGenerator(rescale=1. / 255)
test_set = train_datagen.flow_from_directory('C:/Users/Renato/OneDrive/Ambiente de Trabalho/Datasets/test_set',
                                             target_size=(64, 64),
                                             batch_size=5,
                                             class_mode='binary')

# Training the model
classifier.fit(training_set,
               steps_per_epoch=5,
               epochs=25,
               validation_data=test_set,
               validation_steps=10)

# Let's make predictions
test_image = image.load_img('dog.png', target_size=(64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
results = classifier.predict(test_image)
training_set.class_indices


if results[0][0] == 1:
    prediction = 'dog'
else:
    prediction = "cat"

print(results)
print(prediction)