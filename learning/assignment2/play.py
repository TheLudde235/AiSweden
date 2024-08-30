import numpy as np
import matplotlib.pyplot as plt
import tensorflow.keras

x_train, x_test, y_train, y_test = createDataset()

#TODO:
name = 'Your Name'
imageToTest = 145 # Which image to show. Values from 0 to 999
#ENDTODO

# Used to print
plt.figure()
# ax = plt.subplot(2, 1, 1)
plt.imshow(x_test[imageToTest].reshape(28, 28))
plt.gray()
plt.title('number to test:')
# ax.get_xaxis().set_visible(False)
# ax.get_yaxis().set_visible(False)

model = tensorflow.keras.models.load_model(name + '_model.h5') # Load the model
prediction = model.predict(x_test) # We predict all the test images
predictedNumber = np.where(prediction[imageToTest] == np.amax(prediction[imageToTest]))  # The right image prediction is selected

# Used to print
# ax = plt.subplot(2, 1, 2)
# plt.title('It is a ' + str(predictedNumber[0]))
# ax.get_xaxis().set_visible(False)
# ax.get_yaxis().set_visible(False)
plt.text(11, 26, 'It is a ' + str(predictedNumber[0]), color='white')
plt.show()
