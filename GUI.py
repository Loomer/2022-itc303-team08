import tkinter as tk # Library for GUI
import os
from tkinter import filedialog as fd # for opening file window
from tkinter import ttk # improve button appearance
from tkinter import Canvas
from PIL import ImageTk, Image
from datetime import datetime # for timestamp
import time
from fpdf import FPDF

LARGE_FONT = ("Verdana", 16) # define large font for GUI

img_path = '' # Image path for analysis

destination_path = '' # intial destination folder location

dateTimeObj = datetime.now() # get timestamp

class LungXapp(tk.Tk): # class for application

    def __init__(self, *args, **kwargs): # excute on call
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "LungX") # Window Title
        tk.Tk.wm_geometry(self, '800x600') # Window Dimensions

        container = tk.Frame(self) # to display frames in
        
        # container formatting
        container.pack(side = "top", fill = "both", expand = "True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ResultsPage): # All different frames

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(StartPage) # Show StartPage on start up

    def show_frame(self, cont): # Method to push frame to the top
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame): # Arrange Start Page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        title = tk.Label(self, text="LungX", font=LARGE_FONT) # Title in Frame
        title.place(relx=.5, rely=.1,anchor= tk.CENTER) # Position in centre on x-axis and 10% down y-axis

        filename_label = tk.Label(self, text = '') # Label for Filename after selection\

        # Create button and assign functions
        upload_button = ttk.Button(self, text="Upload File...",
                                   command=lambda:[
                                       # called on button click file select,
                                       # reposition upload button and add analyse button                                       # 
                                       select_file(),
                                       filename_label.config(text = img_path),
                                       filename_label.place(relx=.5, rely=.65,anchor= tk.CENTER),
                                       upload_button.place(relx=.4, rely=.7,anchor= tk.CENTER),
                                       analyse_button.place(relx=.6, rely=.7,anchor= tk.CENTER),
                                       canvas.create_image(0, 0, anchor=tk.NW ,image=load_image(img_path, self))
                                       ])

        # Create analysis button
        analyse_button = ttk.Button(self, text="Analyse Image...",
                                    #command swaps to results frame
                            command=lambda: [controller.show_frame(ResultsPage)])

        # Intial placement of Upload button
        upload_button.place(relx=.5, rely=.7,anchor= tk.CENTER)

        # Display Image
        canvas = Canvas(self, width = 250, height = 250)  
        canvas.place(relx=.5, rely=.4,anchor= tk.CENTER)

 
# image selection method. Opens a window in File explorer and saves selected image's filepath
# global image filepath iable
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
    global destination_path
    
    img_path = filename
    destination_path = os.path.dirname(img_path)
    print(destination_path)


def load_image(path, root):
    img = Image.open(path)
    img = img.resize((250, 250))
    imgtk = ImageTk.PhotoImage(img)
    root.imgtk = imgtk # to prevent the image garbage collected.
    return imgtk

def generate_report(path):

    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    pdf.set_font("Arial", size = 20)

    # create a cell
    pdf.cell(200, 20, txt = "LungX Report",
                    ln = 1, align = 'L')

    pdf.set_font("Arial", size = 12)

    # add another cell
    pdf.cell(200, 10, txt = "Image URL: " + path,
                    ln = 2, align = 'L')

    pdf.image(path, 15, 40, 110, 110)

    timestr = time.strftime("%Y%m%d_%H%M%S")

    pdf.output(timestr + 'lungxreport.pdf')


# for results of assessments
class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        title = tk.Label(self, text="LungX COVID Pneumonia Screening Report", font=LARGE_FONT)
        title.place(relx=.5, rely=.1,anchor= tk.CENTER)

        filename_label = tk.Label(self, text = img_path)
        filename_label.place(relx=.5, rely=.6,anchor= tk.CENTER)


        severity_label = tk.Label(self, text="Report Findings: ")
        severity_label.place(relx=.5, rely=.7,anchor= tk.CENTER)

        # Display Image
##        canvas = Canvas(self, width = 250, height = 250)  
##        canvas.place(relx=.5, rely=.4,anchor= tk.CENTER)
##        canvas.create_image(0, 0, anchor=tk.NW ,image=load_image(img_path, self))

        # Display timestamp on report generation
        timestamp = tk.Label(self, text= str(dateTimeObj))
        timestamp.place(relx=.5, rely=.55,anchor= tk.CENTER)

        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx=.4, rely=.9,anchor= tk.CENTER)

        button2 = ttk.Button(self, text="Save Report",
                            command=lambda: generate_report(img_path))
        button2.place(relx=.6, rely=.9,anchor= tk.CENTER)
        
        destination_title = tk.Label(self, text = "Destination Folder (Original image location by default): ")
        destination_title.place(relx=.5, rely=.7,anchor= tk.CENTER)
        
        destination_label = tk.Label(self, text = destination_path)
        destination_label.place(relx=.5, rely=.75,anchor= tk.CENTER)

        button3 = ttk.Button(self, text="Change...",
                            command=lambda:[askdir(), destination_label.config(text = destination_path), destination_label.place(relx=.5, rely=.75,anchor= tk.CENTER)])
                                             
        button3.place(relx=.5, rely=.8,anchor= tk.CENTER)

def askdir():
  dirname = fd.askdirectory()
  global destination_path

  destination_path = dirname
  print(destination_path)

# Run app
app = LungXapp()
app.mainloop()
