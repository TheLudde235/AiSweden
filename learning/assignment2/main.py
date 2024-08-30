from functions import *
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import numpy as np

#TODO: Write your full name.
name = 'Ludvig'
#ENDTODO

x_train, x_test, y_train, y_test = createDataset()

imageSize = 784 # Each image has a total of 784 pixels
numClasses = 10 # We have 10 different numbers

model = Sequential() # The model is initialized

#TODO: Add/Remove layers to the model: model.add(Dense(units = numberUnits, activation= trainingMethod)).
# You have to set numberUnits and activation function for each layer.
#   numberUnits: It shold be a number between inputSize (784) and numClasses (10). The number of units in layer one is higher than the units in layer 2.
#   trainingModels Options:
#       - 'sigmoid'
#       - 'relu'
#       - 'tanh'
model.add(Dense(units = 784, activation='relu', input_shape=(imageSize,)))
model.add(Dense(units = 392, activation='tanh', input_shape=(imageSize,)))
model.add(Dense(units = 120, activation='sigmoid', input_shape=(imageSize,)))
# model.add(Dense(units = 32, activation= 'sigmoid'))
# ...
# ENDTODO
model.add(Dense(units=numClasses, activation='softmax')) # Output layer. DO NOT CHANGE!
model.summary() # It will print how the network looks like

# TODO: Setup the training Options
optimizerFunction = 'adam'# Options: 'sgd', 'adam', 'adamax', 'adadelta'
batchSize = 1000 #How many training images are taken at the same time. Possitive integer, smaller than 1000
epochsNumber = 50
#ENDTODO

model.compile(optimizer=optimizerFunction, loss='categorical_crossentropy', metrics=['accuracy']) # We set the training options
history = model.fit(x_train, y_train, batch_size=batchSize, epochs=epochsNumber, verbose=True, validation_split=.1) # We train the model
loss, accuracy  = model.evaluate(x_test, y_test, verbose=False) # We evaluate the model

saveAndPrintResults(model, name, history, accuracy) # This function will save the model and results
