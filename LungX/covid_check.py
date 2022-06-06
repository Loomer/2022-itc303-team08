#Importing necessary modules
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2


#Function to check presence of covid pneumonia type
def covid_check(link):

    #Creating an interpreter for the tf lite file and allocating sensors
    interpreter = tf.lite.Interpreter("cnn/tf_lite_model.tflite") 
    interpreter.allocate_tensors()
  
    #Processing the image to work with the model
    img = cv2.imread(link)
    test_image = cv2.resize(img, (250,250)) 
    test_image = np.expand_dims(test_image, axis=0).astype(np.float32)

    #Setting requirements for the interpreter
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]
    interpreter.set_tensor(input_index, test_image)

    #Predicting the image type
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_index) 

    # returns 1 or 0 based on prediction
    if (str(predictions)[2] == "0"): # negative result
        return 0
    elif (str(predictions)[2] == "1"): # positive result
        return 1
