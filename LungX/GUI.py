import tkinter as tk # Library for GUI
import os
import time
from covid_check import covid_check
from tkinter import filedialog as fd # for opening file window
from tkinter import ttk # improve button appearance
from tkinter import Canvas
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

# pre written report findings based on image analysis results
pos_result_str = """Signs of COVID-19 pneumonia found in patient lungs.\n
Results suggest patient is COVID-19 positive or is still experiencing
residual symptoms of COVID-19 pneumonia."""

# ditto
neg_result_str = """No sign of COVID-19 pneumonia found in patient lungs.\n
Results suggest patient is COVID-19 negative and is not experiencing symptoms of COVID-19 pneumonia."""

class LungXapp(tk.Tk): # class for application

    def __init__(self, *args, **kwargs): # excute on call
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "LungX") # Window Title
        tk.Tk.wm_geometry(self, '800x600') # Window Dimensions

        self.iconbitmap("icon.ico") # set icon
        self.container = tk.Frame(self) # insert container into frame
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.show_frame(StartPage) # show startpage

    def show_frame(self, new_frame_class): #show new frame and refresh
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)





# -------------------------------------------Frames------------------------------------------- #





class StartPage(tk.Frame): # Arrange Start Page

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        title = tk.Label(self, text="LungX", font=LARGE_FONT) # Title in Frame
        title.place(relx=.5, rely=.1,anchor= tk.CENTER) # Position in centre on x-axis and 10% down y-axis

        filename_label = tk.Label(self, text = '') # Label for Filename after selection

        # Create button and assign functions
        upload_button = ttk.Button(self, text="Upload File",
                                   command=lambda:[
                                       # called on button click file select,
                                       select_file(),
                                       # reposition upload button and add analyse button
                                       upload_button_command(self, filename_label, upload_button, analyse_button, canvas)
                                       ])

        # Create analysis button
        analyse_button = ttk.Button(self, text="Analyse Image",
                                    #command swaps to results frame
                                    # call cnn function
                            command=lambda: [analyse_image(img_path), controller.show_frame(ResultsPage)])

        # Intial placement of Upload button
        upload_button.place(relx=.5, rely=.7,anchor= tk.CENTER)

        # Display Image
        canvas = Canvas(self, width = 250, height = 250)  
        canvas.place(relx=.5, rely=.4,anchor= tk.CENTER)
    

# for results of assessments
class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create scroll window
        container = self
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
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
        destination_title = tk.Label(self, text = "Destination Folder (Original image location by default): ", font = "Helvetica 12 bold").pack(padx= 20, anchor = "w") # 'pack' insert label

        # string var for updating folder directory label
        var = tk.StringVar()
        var.set(destination_path)

        # folder directory label
        destination_label = tk.Label(self, textvariable = var).pack(padx= 20, anchor = "w")

        # change destination folder button
        button1 = ttk.Button(self, text="Change Destination Folder",
                            command=lambda:[askdir(), var.set(destination_path)])

        button1.pack(padx= 20, pady=5, anchor = "w")


        # save report button calls pdf save method
        # gets textbox contents for report generation
        button2 = ttk.Button(self, text="Save Report",
                            command=lambda: [get_textbox_input(user_comments_text),
                                             generate_report(result),
                                             tk.messagebox.showinfo("LungX", fname + " saved to " + destination_path) ]).pack(padx= 20, pady=5,anchor = "w")

        # navigate back to startpage
        button3 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage)).pack(padx= 20, pady=5, anchor = "w")

        # seperate pdf preview and previous widgets
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x')        

        # report title
        title = tk.Label(scrollable_frame, text="LungX COVID-19 Pneumonia Screening Report", font=LARGE_FONT).pack(padx= 20, pady=20, anchor = "w")

        # insert image path
        img_path_label = tk.Label(scrollable_frame, text=img_path).pack(padx= 20, anchor = "w")
        # insert timestamp
        timestamp_label = tk.Label(scrollable_frame, text= time.strftime("%A, %d %B %Y, %I:%M:%S %p (%Z; UTC%z)")).pack(padx= 20, anchor = "w")

        # insert image that was uploaded
        img_canvas = Canvas(scrollable_frame, width = 250, height = 250)
        img_canvas.pack(padx = 20, pady=10, anchor = "w")
        img_canvas.create_image(0, 0, anchor=tk.NW, image=load_image(img_path, self))

        # insert report findings title label
        report_findings_label = tk.Label(scrollable_frame, text= "Report Findings", font = "Helvetica 12 bold").pack(padx= 20, pady=20, anchor = "w")

        print(result)

        # insert pre-prepared report findings based on covid_check func from covid_check.py
        report_findings_txt = tk.Label(scrollable_frame, justify = tk.LEFT, text = result)
        
        report_findings_txt.pack(padx= 20, anchor = "w")

        # insert user comments title label
        user_comments_label = tk.Label(scrollable_frame, text= "User Comments", font = "Helvetica 12 bold").pack(padx= 20, pady=20, anchor = "w")

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

    # set image path and destination folder directory
    img_path = filename
    destination_path = os.path.dirname(img_path)
    print(destination_path)

# returns a resized image to display in both frames
def load_image(path, root):
    img = Image.open(path)
    img = img.resize((250, 250))
    imgtk = ImageTk.PhotoImage(img)
    root.imgtk = imgtk # to prevent the image garbage collected.
    return imgtk


# Function to export a report based on report preview in resultspage frame
def generate_report(result):

    global fname

    # timestamp string for file name
    timestr = time.strftime("%Y%m%d_%H%M%S")
    
    # contruct filename
    fname = timestr + 'lungxreport.pdf'

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
    pdf.image(img_path, 15, 50, 110, 110)

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
    pdf.output(destination_path + "/" + fname)

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
def upload_button_command(root, filename_label, upload_button, analyse_button, canvas):

    #if img_path variable is not modified no changes are made to the frame
    if(img_path == ''):
        pass
    # if a valid imag url is entered 
    elif(os.path.exists(img_path)):

        # reposition upload button and add analyse button and display image uploaded image
        filename_label.config(text = img_path)
        filename_label.place(relx=.5, rely=.65,anchor= tk.CENTER)
        upload_button.place(relx=.4, rely=.7,anchor= tk.CENTER)
        analyse_button.place(relx=.6, rely=.7,anchor= tk.CENTER)
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
                  
    
# Run app
app = LungXapp()
app.mainloop()
