import tkinter as tk # Library for GUI
import os
from tkinter import filedialog as fd # for opening file window
from tkinter import ttk # improve button appearance
from tkinter import Canvas
from PIL import ImageTk, Image
from datetime import datetime # for timestamp
import time
from time import strftime
from fpdf import FPDF

LARGE_FONT = ("Verdana", 16) # define large font for GUI

img_path = '' # Image path for analysis

destination_path = '' # intial destination folder location

user_comments = "" # global variable for user comments

dateTimeObj = datetime.now() # get timestamp

fname = ''

pos_result_str = """Signs of COVID-19 pneumonia found in patient lungs.\n
Results suggests patient is COVID-19 positive or is still experiencing
residual symptoms of COVID-19 pneumonia."""

neg_result_str = """No sign of COVID-19 pneumonia found in patient lungs.\n
Results suggests patient is COVID-19 negative and is not experiencing symptoms of COVID-19 pneumonia."""

class LungXapp(tk.Tk): # class for application

    def __init__(self, *args, **kwargs): # excute on call
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "LungX") # Window Title
        tk.Tk.wm_geometry(self, '800x600') # Window Dimensions

        self.iconbitmap("icon.ico") 
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.show_frame(StartPage)

    def show_frame(self, new_frame_class):
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

        filename_label = tk.Label(self, text = '') # Label for Filename after selection\

        # Create button and assign functions
        upload_button = ttk.Button(self, text="Upload File...",
                                   command=lambda:[
                                       # called on button click file select,
                                       # reposition upload button and add analyse button
                                       select_file(),
                                       upload_button_command(self, filename_label, upload_button, analyse_button, canvas)
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
    
    
# for results of assessments
class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        destination_title = tk.Label(self, text = "Destination Folder (Original image location by default): ", font = "Helvetica 12 bold").pack(padx= 20, anchor = "w")

        var = tk.StringVar()
        var.set(destination_path)
        
        destination_label = tk.Label(self, textvariable = var).pack(padx= 20, anchor = "w")

        button1 = ttk.Button(self, text="Change Destination Folder...",
                            command=lambda:[askdir(), var.set(destination_path)])

        button1.pack(padx= 20, pady=5, anchor = "w")

        button2 = ttk.Button(self, text="Save Report",
                            command=lambda: [get_textbox_input(user_comments_text),
                                             generate_report(result),
                                             tk.messagebox.showinfo("LungX", fname + " saved to " + destination_path) ]).pack(padx= 20, pady=5,anchor = "w")

        button3 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage)).pack(padx= 20, pady=5, anchor = "w")

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x')        

        title = tk.Label(scrollable_frame, text="LungX COVID-19 Pneumonia Screening Report", font=LARGE_FONT).pack(padx= 20, pady=20, anchor = "w")

        img_path_label = tk.Label(scrollable_frame, text=img_path).pack(padx= 20, anchor = "w")
        timestamp_label = tk.Label(scrollable_frame, text= time.strftime("%A, %d %B %Y, %I:%M:%S %p (%Z; UTC%z)")).pack(padx= 20, anchor = "w")

        img_canvas = Canvas(scrollable_frame, width = 250, height = 250)
        img_canvas.pack(padx = 20, pady=10, anchor = "w")
        img_canvas.create_image(0, 0, anchor=tk.NW, image=load_image(img_path, self))

        report_findings_label = tk.Label(scrollable_frame, text= "Report Findings", font = "Helvetica 12 bold").pack(padx= 20, pady=20, anchor = "w")

        result = ''
        res = 1

        if res == 1:
            result = pos_result_str
        elif res == 0:
            result = neg_result_str

        report_findings_txt = tk.Label(scrollable_frame,
                                       justify = tk.LEFT,
                                       text = result)
        
        report_findings_txt.pack(padx= 20, anchor = "w")

        user_comments_label = tk.Label(scrollable_frame, text= "User Comments", font = "Helvetica 12 bold").pack(padx= 20, pady=20, anchor = "w")

        user_comments_text = tk.Text(scrollable_frame, height = 10, width = 80)
        user_comments_text.insert(tk.END, "")
        user_comments_text.pack(padx= 20, anchor = "w")

        progx_label = tk.Label(scrollable_frame, text= "ProgX \u00a9", font = "Helvetica 12 bold").pack(pady=30, anchor = "s")

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        


# -------------------------------------------Functions------------------------------------------- #




# image selection method. Opens a window in File explorer and saves selected image's filepath
# global image filepath iable
def select_file():
    filetypes = ( # file type resttrictions
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
    
    img_path = filename
    destination_path = os.path.dirname(img_path)
    print(destination_path)


def load_image(path, root):
    img = Image.open(path)
    img = img.resize((250, 250))
    imgtk = ImageTk.PhotoImage(img)
    root.imgtk = imgtk # to prevent the image garbage collected.
    return imgtk



def generate_report(result):

    global fname

    timestr = time.strftime("%Y%m%d_%H%M%S")
    
    fname = timestr + 'lungxreport.pdf'

    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    pdf.set_font("Arial", size = 20)

    # create a cell
    pdf.cell(200, 20, txt = "LungX COVID-19 Pneumonia Screening Report",
                    ln = 1, align = 'L')

    pdf.set_font("Arial", size = 12)
    pdf.cell(220, 10, txt = img_path, ln = 2, align = 'L')

    pdf.cell(220, 10, txt = time.strftime("%A, %d %B %Y, %I:%M:%S %p (%Z; UTC%z)"), ln = 2, align = 'L')
    
    pdf.image(img_path, 15, 50, 110, 110)

    pdf.cell(220, 120, txt = "", ln = 1, align = 'L')

    pdf.set_font("Arial", 'B' ,size = 12)
    pdf.cell(220, 10, txt = "Report Findings", ln = 1, align = 'L')

    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(180.0, 5.0, txt = result, border = 0, 
                align= 'L', fill = False)

    pdf.set_font("Arial", 'B' ,size = 12)
    pdf.cell(1, 1, txt = "", ln = 1, align = 'L')
    pdf.cell(220, 10, txt = "User Comments", ln = 1, align = 'L')
    
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(180.0, 5.0, txt = user_comments, border = 0, 
                align= 'J', fill = False)

    pdf.text(x = 100.0, y = 280.0, txt = "ProgX \u00a9")

    pdf.output(destination_path + "/" + fname)


def askdir():
  dirname = fd.askdirectory()
  global destination_path

  destination_path = dirname
  
  print(destination_path)

def get_textbox_input(user_comments_text):
    global user_comments 
    user_comments = user_comments_text.get("1.0", "end-1c")

def upload_button_command(root, filename_label, upload_button, analyse_button, canvas):

    if(img_path == ''):
        pass
    
    elif(os.path.exists(img_path)):

        filename_label.config(text = img_path)
        filename_label.place(relx=.5, rely=.65,anchor= tk.CENTER)
        upload_button.place(relx=.4, rely=.7,anchor= tk.CENTER)
        analyse_button.place(relx=.6, rely=.7,anchor= tk.CENTER)
        canvas.create_image(0, 0, anchor=tk.NW ,image=load_image(img_path, root))

    else:
        pass

# Run app
app = LungXapp()
app.mainloop()
