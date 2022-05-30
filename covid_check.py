import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
print("hello")

def create_model():
  model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(250, 250, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation=tf.nn.relu), 
    tf.keras.layers.Dense(2, activation=tf.nn.softmax)])
  
  
  model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

  print("done")
  return model

model = create_model()
model.summary()

loaded_model = load_model("C:/Users/manve/Desktop/new_model.h5")
loaded_model.summary()

path = "C:/Users/manve/Desktop/ml-images/test-normal-2.png"
img = cv2.imread(path)
test_image = cv2.resize(img, (250,250))
test_image = np.expand_dims(test_image, axis=0)
images = np.vstack([test_image])
prediction = loaded_model.predict(images)
print(prediction)
print(type(prediction))
print(np.argmax(prediction[0]))
