#import the libraries
import cv2 as cv
import numpy as np
from PIL import Image
import os

#Function to implement the new feature
#Takes in an image and returns a numpy array of the product image
def highlighter(img):

    #Using the masked function on the image
    masked(img)

    #Taking the two images to use
    img1 = cv.imread("img1.png")
    img2 = cv.imread("img2.png")

    #Processsing them to get a new image
    dst = cv.addWeighted(img1,1,img2,1,0)

    #Saving the image
    data = Image.fromarray(dst)
    data.save('img3.png')

    process_image("img3.png")

    #Taking two images to process
    img5 = cv.imread(img)
    img6 = cv.imread("img4.png")

    #Processsing them to get a new image
    dst = cv.addWeighted(img5,1,img6,0.2,0)

    #Removing the images
    os.remove("img1.png")
    os.remove("img2.png")
    os.remove("img3.png")
    os.remove("img4.png")

    #Saving the image
    data = Image.fromarray(dst)
    data.save('output.png')

    '''#Returning the numpy array
    return dst'''

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

def process_image(image):

    #Declaring variables to use in the function
    count = 0
    total_count = 0
    color1 = (0, 0, 0)
    color2 = (255, 255, 255)
    new_color = (0, 0, 255)
    img = Image.open(image).convert('RGB')
    w, h = img.size

    #Looping through the image and processing the pixels
    for i in range(w):
        for j in range((int)(h*0.20)):
            current_color = img.getpixel( (i,j) )
            if current_color == color2:
                img.putpixel( (i,j), color1)

    #Looping through the image and processing the pixels
    for i in range(w):
        for j in range((int)(h*0.20), h):
            current_color = img.getpixel( (i,j) )
            if current_color == color2:
                img.putpixel( (i,j), color1)
            if current_color == color1:
                img.putpixel( (i,j), new_color)

    #Looping through the image and processing the pixels
    for i in range((int)(w*0.1)):
        for j in range(h):
            current_color = img.getpixel( (i,j) )
            if current_color == new_color:
                img.putpixel( (i,j), color1)

    #Looping through the image and processing the pixels
    for i in range((int)(w*0.9), w):
        for j in range(h):
            current_color = img.getpixel( (i,j) )
            if current_color == new_color:
                img.putpixel( (i,j), color1)
    img.save("img4.png")

highlighter("C:/Users/manve/Desktop/ml-images/covid_image_github.png")
'''image = highlighter("C:/Users/manve/Desktop/ml-images/covid_image_github.png")
print(type(image))
cv.imshow('', image)'''
