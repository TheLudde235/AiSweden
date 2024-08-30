from keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import keras
import tensorflow

# Function: It will load the train and test datasets
# Outputs:
#   x_train: Each row holds each pixel of an image. Used during training
#   x_test: Each row holds each pixel of an image. Used to test the model
#   y_train: It will indicate which number is each row in x_train
#   y_test: It will indicate which number is each row in y_train
def createDataset():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    #Reshape
    image_vector_size = 28*28
    x_train = x_train.reshape(x_train.shape[0], image_vector_size)
    x_test = x_test.reshape(x_test.shape[0], image_vector_size)

    #Normalization
    x_train = x_train / 255
    x_test = x_test / 255

    # One-hot encoding
    num_classes = 10
    y_train = tensorflow.keras.utils.to_categorical(y_train, num_classes)
    y_test = tensorflow.keras.utils.to_categorical(y_test, num_classes)

    return x_train, x_test, y_train, y_test

# Function: This function whil save a pring the results
# Inputs:
#   model: A neural network that have been trained
#   name: Your name to be used in the name of the file and the model
#   history: It holds the results during training
#   accuracy: The percentage of correct guesses by the Artificial Neural Network
def saveAndPrintResults(model, name, history, accuracy):
    print(f'\n\nTest accuracy: {(accuracy*100):.6}%')

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title(name+'\'s model accuracy('+str(accuracy*100)+'%)')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['training', 'validation'], loc='best')

    # model.save(name + '_model.h5')
