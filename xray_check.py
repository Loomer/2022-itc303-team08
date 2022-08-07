#Importing necessary modules
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
#import tf.keras.preprocessing.image
from PIL import Image
import numpy as np
import cv2

#Creating an interpreter for the tf lite file and allocating sensors
interpreter = tf.lite.Interpreter("tflite_checker_fp16")
interpreter.allocate_tensors()

def is_Xray(path):
    count = 0
    total_count = 0
    img = Image.open(path).convert('RGB')
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            toral_count = total_count + 1
            if r != g != b:
                count = count + 1
                
    acceptable_value = total_count/20
    if count > acceptable_value:
        return False           
    else:
        return True

#Function to check lung type
def xray_check(link):
  
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
  if (np.argmax(predictions[0]) == 0):
    return True
  elif (np.argmax(predictions[0]) == 1):
    return False

print("Please enter a valid lung Xray image")
response = input("Enter link")
if (is_Xray(response) & xray_check(response) == True):
    print("VALID XRAY IMAGE")
else:
    print("INVALID IMAGE")
        
'''answer = is_Xray("C:/Users/manve/Desktop/LungX_EA/LungX_EA/NORMAL1.jpeg")
ans = xray_check("C:/Users/manve/Desktop/LungX_EA/LungX_EA/NORMAL1.jpeg")
print(answer, ans)'''
