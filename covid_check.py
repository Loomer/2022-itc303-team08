import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2

def covid_check(link):
  model = load_model("C:/Users/manve/Desktop/ml-images/github/2022-itc303-team08/new_model.h5")
  path = link
  img = cv2.imread(path)
  test_image = cv2.resize(img, (250,250))
  test_image = np.expand_dims(test_image, axis=0)
  images = np.vstack([test_image])
  prediction = model.predict(images)
  return np.argmax(prediction[0])

temp = input("Please enter path")
print(covid_check(temp))
