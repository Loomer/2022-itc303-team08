import tkinter as tk # Library for GUI
from tkinter import filedialog as fd # for opening file window
from tkinter import ttk # improve button appearance
from tkinter import scrolledtext
from tkinter import *
import PIL as pil
from PIL import Image, ImageTk
import tensorflow as tf
from datetime import datetime # for timestamp
import cv2
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

#Creating an interpreter for the tf lite file and allocating sensors
interpreter = tf.lite.Interpreter("C:/Users/lachl/OneDrive/Desktop/LungX_EA/tflite_model_fp16.tflite") 
interpreter.allocate_tensors()

LARGE_FONT = ("Verdana", 16) # define large font for GUI

img_path = '' # Image path for analysis

dateTimeObj = datetime.now() # get timestamp

result = 'empty' # For storing result

#Function to check lung type
def covid_check(link):
  
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

  global result
  result = "NORMAL" if str(predictions)[2] == "0" else "COVID"
  return result

class LungXapp(tk.Tk): # class for application

    def __init__(self, *args, **kwargs): # excute on call
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "LungX") # Window Title
        tk.Tk.wm_geometry(self, '800x450') # Window Dimensions

        container = tk.Frame(self) # to display frames in
        
        # container formatting
        container.pack(side = "top", fill = "both", expand = "True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) # Show StartPage on start up

    def show_frame(self, cont): # Method to push frame to the top
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame): # Arrange Start Page

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        title = tk.Label(self, text="LungX", font=LARGE_FONT) # Title in Frame
        title.place(relx=.5, rely=.1,anchor= tk.CENTER) # Position in center on x-axis and 10% down y-axis

        filename_label = tk.Label(self, text = '') # Label for Filenaem after selection

        label = tk.Label(self, text = "Result: ")
        label.place(relx=.15, rely=.3,anchor= tk.CENTER)

        img = Image.open("default.jpg")
        image1 = img.resize((250, 250))
        test = ImageTk.PhotoImage(image1)

        label1 = tk.Label(image=test)
        label1.image = test

        entrybox = scrolledtext.ScrolledText(self, wrap=tk.WORD, height = 20, width = 30)

        # Position image
        label1.place(relx=.4, rely=.5,anchor= tk.CENTER)
        
        # Create button and assign functions
        upload_button = ttk.Button(self, text="Upload File...",
                                   command=lambda:[
                                       # called on button click file select,
                                       # reposition upload button and add analyse button                                       # 
                                       select_file(),
                                       filename_label.config(text = img_path),
                                       filename_label.place(relx=.5, rely=.15,anchor= tk.CENTER),
                                       upload_button.place(relx=.15, rely=.4,anchor= tk.CENTER),
                                       analyse_button.place(relx=.15, rely=.5,anchor= tk.CENTER),
                                       showImage(img_path)
                                       ])
        
        # Create analysis button
        analyse_button = ttk.Button(self, text="Analyse Image...",
                                    #command swaps to results frame
                            command=lambda: [
                                label.config(text = "Result: " + covid_check(img_path)),
                                addComment_button.place(relx=.15, rely=.6, anchor = tk.CENTER)])


        # Create SaveFile button
        saveComment_button = ttk.Button(self, text="Save File to root folder",
                                    #command swaps to results frame
                            command=lambda: [
                                saveText(img_path),
                                quit()])

        # Create AddComment button
        addComment_button = ttk.Button(self, text="Add Comment",
                                    #command swaps to results frame
                            command=lambda: [
                                saveComment_button.place(relx=.55, rely=.89, anchor = tk.CENTER),
                                entrybox.place(relx =.8, rely=.55, anchor = tk.CENTER)])
                                        

        # Intial placement of Upload button
        upload_button.place(relx=.15, rely=.4,anchor= tk.CENTER)

        def showImage(link):
            img = Image.open(link)
            image1 = img.resize((250, 250))
            test = ImageTk.PhotoImage(image1)

            label1 = tk.Label(image=test)
            label1.image = test
            label1.place(relx=.4, rely=.5,anchor= tk.CENTER)

        def saveText(link):
            text_file = open(link + "_LUNGX_Report.txt", "w")
            text_file.write("LungX Report for:" + link + "\n")
            text_file.write("\n\nUser Comments:\n")
            text_file.write(entrybox.get(1.0, END))
            text_file.write("\n\n" + str(datetime.now()))
            text_file.close()
        
# image selection method. Opens a window in File explorer and saves selected image's filepath
# global image filepath variable
def select_file():
    filetypes = ( # file type resttrictions
        ('JPEG', '*.jpg'),
        ('JPEG', '*.jpeg'),
        ('PNG', '*.png'),
        ('Images', '*.jpg'),
        ('Images', '*.jpeg'),
        ('Images', '*.png'),
    )

    
    filename = fd.askopenfilename( # open window
        title='Open a file',
        initialdir='/Pictures',
        filetypes=filetypes)

    global img_path
    img_path = filename


    
# Run app
app = LungXapp()
app.mainloop()
