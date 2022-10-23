import tkinter as tk
import customtkinter
import os
import time
import cv2 as cv
import numpy as np
from covid_check import covid_check
from xray_check import is_Xray
from xray_check import xray_check
from tkinter import filedialog as fd # for opening file window
from tkinter import ttk # improve button appearance
from tkinter import Canvas
from customtkinter import CTkButton
from customtkinter import CTkLabel
from PIL import ImageTk, Image
from datetime import datetime # for timestamp
from time import strftime
from fpdf import FPDF

LARGE_FONT = ("Verdana", 16) # define large font for GUI

img_path = '' # Image path for analysis

destination_path = '' # intial destination folder location

user_comments = "" # global variable for user comments

dateTimeObj = datetime.now() # get timestamp

fname = '' # filename variable for message box

result = '' # for report findings

res = None # variable for future 'if' statement

res_proc = None

# pre written report findings based on image analysis results
pos_result_str = """Signs of COVID-19 pneumonia found in patient lungs.\n
Results suggest patient is COVID-19 positive or is still experiencing
residual symptoms of COVID-19 pneumonia."""

# ditto
neg_result_str = """No sign of COVID-19 pneumonia found in patient lungs.\n
Results suggest patient is COVID-19 negative and is not experiencing symptoms of COVID-19 pneumonia."""

# pre written validity reports based on image check results
valid_result_str = """Image is a valid xray"""
invalid_result_str = """Image is not a valid xray"""

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class LungXapp(customtkinter.CTk): # class for application

    def __init__(self): # excute on call


        super().__init__()

        
        self.title("LungX") # Window Title
        self.geometry('800x600') # Window Dimensions

        self.iconbitmap("icon.ico") # set icon
        self.container = customtkinter.CTkFrame(self) # insert container into frame
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.show_frame(StartPage) # show startpage

        self.resizable(False,False) #  Make the window resizable false

    def show_frame(self, new_frame_class): #show new frame and refresh
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)





# -------------------------------------------Frames------------------------------------------- #





class StartPage(customtkinter.CTkFrame): # Arrange Start Page

    def __init__(self, parent, controller):

        customtkinter.CTkFrame.__init__(self, parent)
        
        title = customtkinter.CTkLabel(self, text="LungX") # Title in Frame
        title.place(relx=.5, rely=.1,anchor= tk.CENTER) # Position in centre on x-axis and 10% down y-axis

        filename_label = customtkinter.CTkLabel(self, text = '') # Label for Filename after selection
        filecheck_label = customtkinter.CTkLabel(self, text = '') #  Label for displaying error message if file not an Xray

        # Create button and assign functions
        upload_button = customtkinter.CTkButton(master=self, text="Upload File",
                                   command=lambda:[
                                       # called on button click file select,
                                       select_file(),
                                       # reposition upload button and add analyse button
                                       upload_button_command(self, filename_label, filecheck_label, upload_button, analyse_button, canvas)
                                       ])

        # Create analysis button
        analyse_button = customtkinter.CTkButton(self, text="Analyse Image",
                                    #command swaps to results frame
                                    # call cnn function
                            command=lambda: [analyse_image(img_path), controller.show_frame(ResultsPage)])

        # Intial placement of Upload button
        upload_button.place(relx=.5, rely=.7,anchor= tk.CENTER)

        # Display Image
        canvas = Canvas(self, width = 250, height = 250)  
        canvas.place(relx=.5, rely=.4,anchor= tk.CENTER)
        canvas.create_image(0, 0, anchor=tk.NW ,image=load_image("default.jpg", self))
    

# for results of assessments
class ResultsPage(customtkinter.CTkFrame):

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        # create scroll window
        container = self
        
        canvas = tk.Canvas(container)
        scrollbar = customtkinter.CTkScrollbar(container, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # create scroll window 2
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # destination folder title
        destination_title = customtkinter.CTkLabel(self, text = "Destination Folder (Original image location by default): ").pack(padx= 20, anchor = "w") # 'pack' insert label

        # string var for updating folder directory label
        var = tk.StringVar()
        var.set(destination_path)

        # folder directory label
        destination_label = customtkinter.CTkLabel(self, textvariable = var).pack(padx= 20, anchor = "w")

        # change destination folder button
        button1 = customtkinter.CTkButton(self, text="Change Destination Folder",
                            command=lambda:[askdir(), var.set(destination_path)])

        button1.pack(padx= 20, pady=5, anchor = "w")


        # save report button calls pdf save method
        # gets textbox contents for report generation
        button2 = customtkinter.CTkButton(self, text="Save Report",
                            command=lambda: [get_textbox_input(user_comments_text),
                                             generate_report(result, fname),
                                             tk.messagebox.showinfo("LungX", fname + " saved to " + destination_path) ]).pack(padx= 20, pady=5,anchor = "w")

        # navigate back to startpage
        button3 = customtkinter.CTkButton(self, text="Back",
                            command=lambda: controller.show_frame(StartPage)).pack(padx= 20, pady=5, anchor = "w")

        # seperate pdf preview and previous widgets
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x')        

        # report title
        title = tk.Label(scrollable_frame, text="LungX COVID-19 Pneumonia Screening Report:", font=LARGE_FONT).pack(padx= 20, pady=20, anchor = "w")

        # insert image path
        img_path_label = tk.Label(scrollable_frame, text=img_path).pack(padx= 20, anchor = "w")
        # insert timestamp
        timestamp_label = tk.Label(scrollable_frame, text= time.strftime("%A, %d %B %Y, %I:%M:%S %p (%Z; UTC%z)")).pack(padx= 20, anchor = "w")

        # insert image that was uploaded
        image_H = highlighter(img_path)
        res = cv.resize(image_H, dsize=(250, 250), interpolation=cv.INTER_CUBIC)
        #img =  ImageTk.PhotoImage(Image.fromarray(res))
        img2 = Image.fromarray(res)
        img2.save("working_image.jpeg")
        img_canvas = Canvas(scrollable_frame, width = 550, height = 250)
        img_canvas.pack(padx = 20, pady=10, anchor = "w")
        img_canvas.create_image(0, 0, anchor=tk.NW, image=load_image("working_image.jpeg", self))
       # img_canvas.create_image(300, 0, anchor=tk.NW, image=load_image(img_path, self))
        os.remove("working_image.jpeg")
        

        # insert report findings title label
        report_findings_label = tk.Label(scrollable_frame, text= "Report Findings", font = "Helvetica 12 bold").pack(padx= 20, pady=20, anchor = "w")

        print(result)

        # insert pre-prepared report findings based on covid_check func from covid_check.py
        report_findings_txt = tk.Label(scrollable_frame, justify = tk.LEFT, text = result)
        
        report_findings_txt.pack(padx= 20, anchor = "w")

        # insert user comments title label
        user_comments_label = tk.Label(scrollable_frame, text= "User Comments:", font = "Helvetica 12 bold").pack(padx= 20, pady=20, anchor = "w")

        # insert user comments textbox for user comments
        user_comments_text = tk.Text(scrollable_frame, height = 10, width = 80)
        user_comments_text.insert(tk.END, "")
        user_comments_text.pack(padx= 20, anchor = "w")

        # progx footer
        progx_label = tk.Label(scrollable_frame, text= "ProgX \u00a9", font = "Helvetica 12 bold").pack(pady=30, anchor = "s")

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        


# -------------------------------------------Functions------------------------------------------- #




# image selection method. Opens a window in File explorer and saves selected image's filepath
# global image filepath iable
def select_file():
    filetypes = ( # file type restrictions
        ('Images', '*.jpg'),
        ('Images', '*.jpeg'),
        ('Images', '*.png'),
        ('JPEG', '*.jpg'),
        ('JPEG', '*.jpeg'),
        ('PNG', '*.png'),
    )

    
    filename = fd.askopenfilename( # open window

        title='Open a file',
        initialdir='/Pictures',
        filetypes=filetypes)

    global img_path
    global destination_path
    global fname

    # set image path and destination folder directory
    img_path = filename
    destination_path = os.path.dirname(img_path)
    fname = os.path.basename(img_path)
    fname = os.path.splitext(fname)[0]
    print(destination_path)
    print('File name:')
    print(fname)

# returns a resized image to display in both frames
def load_image(path, root):
    img = Image.open(path)
    img = img.resize((250, 250))
    imgtk = ImageTk.PhotoImage(img)
    root.imgtk = imgtk # to prevent the image garbage collected.
    return imgtk

# Function to export a report based on report preview in resultspage frame
def generate_report(result, fname):

    # timestamp string for file name
    timestr = time.strftime("%Y%m%d_%H%M%S")
    
    # contruct filename
    file_name = fname + '_lungxreport.pdf'

    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    pdf.set_font("Arial", size = 20)

    # create a cell for titlr
    pdf.cell(200, 20, txt = "LungX COVID-19 Pneumonia Screening Report",
                    ln = 1, align = 'L')

    # position and insert file path
    pdf.set_font("Arial", size = 12)
    pdf.cell(220, 10, txt = img_path, ln = 2, align = 'L')

    # position and insert timestamp
    pdf.cell(220, 10, txt = time.strftime("%A, %d %B %Y, %I:%M:%S %p (%Z; UTC%z)"), ln = 2, align = 'L')

    # position and insert image
    image_H = highlighter(img_path)
    res = cv.resize(image_H, dsize=(250, 250), interpolation=cv.INTER_CUBIC)
    #img =  ImageTk.PhotoImage(image=Image.fromarray(res))
    img = Image.fromarray(res)
    img.save("HIGHLIGHTED_IMAGE.jpeg")
    pdf.image("HIGHLIGHTED_IMAGE.jpeg", 15, 50, 110, 110)
    os.remove("HIGHLIGHTED_IMAGE.jpeg")
    

    # padding
    pdf.cell(220, 120, txt = "", ln = 1, align = 'L')

    # position and insert report findings title
    pdf.set_font("Arial", 'B' ,size = 12)
    pdf.cell(220, 10, txt = "Report Findings", ln = 1, align = 'L')

    # position and insert report findings 
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(180.0, 5.0, txt = result, border = 0, 
                align= 'L', fill = False)


    # position and insert user comments title
    pdf.set_font("Arial", 'B' ,size = 12)
    pdf.cell(1, 1, txt = "", ln = 1, align = 'L')
    pdf.cell(220, 10, txt = "User Comments", ln = 1, align = 'L')
    
    # position and insert user comments
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(180.0, 5.0, txt = user_comments, border = 0, 
                align= 'J', fill = False)


    # position and insert progX in footer
    pdf.text(x = 100.0, y = 280.0, txt = "ProgX \u00a9")

    # save pdf in selected destination folder
    pdf.output(destination_path + "/" + file_name)

# opens window to select destination folder
# retrieve destination
def askdir():
  dirname = fd.askdirectory()
  global destination_path

  destination_path = dirname
  
  print(destination_path)


# retrieves user comments from text box in report preview
def get_textbox_input(user_comments_text):
    global user_comments 
    user_comments = user_comments_text.get("1.0", "end-1c")


# fucntion to ensure an image is uploaded
def upload_button_command(root, filename_label, filecheck_label, upload_button, analyse_button, canvas):

    #if img_path variable is not modified no changes are made to the frame
    if(img_path == ''):
        pass
    # if a valid imag url is entered 
    elif(os.path.exists(img_path)):
        # check if image valid
        check_image(img_path)
        
        # reposition upload button and add analyse button and display image uploaded image
        filename_label.configure(text = img_path)
        filename_label.place(relx=.5, rely=.65,anchor= tk.CENTER)
        print(res_proc)
        if res_proc == 1:
            upload_button.place(relx=.4, rely=.7,anchor= tk.CENTER)
            analyse_button.place(relx=.6, rely=.7,anchor= tk.CENTER)
            filecheck_label.place_forget()
        elif res_proc == 0:
            analyse_button.place_forget()
            filecheck_label.configure(text = 'WARNING: File selected is not a valid lung Xray', fg="red")
            filecheck_label.place(relx=.5, rely=.75, anchor= tk.CENTER)
            upload_button.place(relx=.5, rely=.7,anchor= tk.CENTER)
        canvas.create_image(0, 0, anchor=tk.NW ,image=load_image(img_path, root))

    else:
        pass


# calls covid check and sets the report findings variable
def analyse_image(path):

    global result
    global res
    global pos_result_str
    global neg_result_str    

    res = covid_check(path) # function uses cnn to determine covid-19 pneumonia presence in x-ray
    print(res)

    #if covid_check returns '1' covid +ve. if '0' covid -ve
    if res == 1:
        result = pos_result_str
        print(result)
    elif res == 0:
        result = neg_result_str
        print(result)

# calls xray check and sets the report findings variable
def check_image(path):

    global result
    global res
    global res_proc
    global valid_result_str
    global invalid_result_str    

    res = is_Xray(path)

    if res == 1:
        res = xray_check(path) # function uses cnn to determine covid-19 pneumonia presence in x-ray
        print('is Xray')
    elif res == 0:
        res = 0
        print('isnt Xray')

    #if xray_check returns '1' image is valid. if '0' image is not valid
    if res == 1:
        result = valid_result_str
        print(result)
        res_proc = 1
    elif res == 0:
        result = invalid_result_str
        print(result)
        res_proc = 0

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

    #Returning the numpy array
    return dst

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
    
# Run app
app = LungXapp()
app.mainloop()
