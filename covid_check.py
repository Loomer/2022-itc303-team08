import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2

"""def covid_check(link):
  model = load_model("C:/Users/manve/Desktop/new_model.h5")
  path = link
  img = cv2.imread(path)
  test_image = cv2.resize(img, (250,250))
  test_image = np.expand_dims(test_image, axis=0)
  images = np.vstack([test_image])
  prediction = model.predict(images)
  return np.argmax(prediction[0])"""

interpreter = tf.lite.Interpreter("C:/Users/manve/Desktop/tflite_model_fp16.tflite")
interpreter.allocate_tensors()


def covid_check(link):
  img = cv2.imread(link)
  test_image = cv2.resize(img, (250,250))
  test_image = np.expand_dims(test_image, axis=0).astype(np.float32)
  input_index = interpreter.get_input_details()[0]["index"]
  output_index = interpreter.get_output_details()[0]["index"]
  interpreter.set_tensor(input_index, test_image)
  interpreter.invoke()
  predictions = interpreter.get_tensor(output_index)
  if (str(predictions)[2] == "0"):
    return "NORMAL"
  elif (str(predictions)[2] == "1"):
    return "COVID"
  
temp = input("Please enter path")
print(covid_check(temp))


