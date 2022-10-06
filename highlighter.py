#import the libraries
import cv2 as cv
import numpy as np
from PIL import Image
import os

def highlighter(img):

  #Using the masked function on the image
  masked(img)

  img1 = cv.imread("img1.png")
  img2 = cv.imread("img2.png")

  dst = cv.addWeighted(img1,1,img2,1,0)

  data = Image.fromarray(dst)
  data.save('img3.png')

def masked(img):

  #read the image
  img = cv.imread(img)

  #convert the BGR image to HSV colour space
  hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

  #set the lower and upper bounds for the hue
  lower = np.array([0,0,0])
  upper = np.array([110,150,150])

  #create a mask using inRange function
  mask = cv.inRange(hsv, lower, upper)

  #perform bitwise and on the original image arrays using the mask
  res = cv.bitwise_not(mask)

  #Saving the image
  data = Image.fromarray(res)
  data.save('img1.png')

  #Doing the same thing again
  lower = np.array([0,0,0])
  upper = np.array([110,90,90])

  #create a mask for green colour using inRange function
  mask = cv.inRange(hsv, lower, upper)

  #perform bitwise and on the original image arrays using the mask
  res = cv.bitwise_not(mask)

  #Saving the image
  data = Image.fromarray(mask)
  data.save('img2.png')

highlighter("C:/Users/manve/Desktop/ml-images/covid_image.png")
