import tkinter as tk # Library for GUI
from tkinter import filedialog as fd # for opening file window
from tkinter import ttk # improve button appearance
#from PIL import ImageTk, Image
from datetime import datetime # for timestamp

LARGE_FONT = ("Verdana", 16) # define large font for GUI

img_path = '' # Image path for analysis

dateTimeObj = datetime.now() # get timestamp

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

        for F in (StartPage, ResultsPage, PageTwo): # All different frames

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
        title.place(relx=.5, rely=.1,anchor= tk.CENTER) # Position in center on x-axis and 10% down y-axis

        filename_label = tk.Label(self, text = '') # Label for Filenaem after selection

        # Create button and assign functions
        upload_button = ttk.Button(self, text="Upload File...",
                                   command=lambda:[
                                       # called on button click file select,
                                       # reposition upload button and add analyse button                                       # 
                                       select_file(),
                                       filename_label.config(text = img_path),
                                       filename_label.place(relx=.5, rely=.6,anchor= tk.CENTER),
                                       upload_button.place(relx=.4, rely=.7,anchor= tk.CENTER),
                                       analyse_button.place(relx=.6, rely=.7,anchor= tk.CENTER)
                                       ])

        # Create analysis button
        analyse_button = ttk.Button(self, text="Analyse Image...",
                                    #command swaps to results frame
                            command=lambda: controller.show_frame(ResultsPage))

        # Intial placement of Upload button
        upload_button.place(relx=.5, rely=.7,anchor= tk.CENTER)

 
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


##    showinfo(
##        title='Selected File',
##        message=filename
##    )


# for results of assessments
class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title = tk.Label(self, text="Severity Report", font=LARGE_FONT)
        title.place(relx=.5, rely=.1,anchor= tk.CENTER)

        filename_label = tk.Label(self, text = img_path)
        filename_label.place(relx=.5, rely=.6,anchor= tk.CENTER)


        severity_label = tk.Label(self, text="Severity Score: ")
        severity_label.place(relx=.5, rely=.7,anchor= tk.CENTER)

        # Display timestamp on report generation
        timestamp = tk.Label(self, text= str(dateTimeObj))
        timestamp.place(relx=.5, rely=.8,anchor= tk.CENTER)

 

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx=.4, rely=.9,anchor= tk.CENTER)

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.place(relx=.6, rely=.9,anchor= tk.CENTER)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 2", font=LARGE_FONT)
        label.grid(row = 0, column = 0, pady = 2, padx = 2)

        button1 = ttk.Button(self, text="Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row = 1, column = 0, pady = 2, padx = 2)

        button2 = ttk.Button(self, text="Results Page",
                            command=lambda: controller.show_frame(ResultsPage))
        button2.grid(row = 2, column = 0, pady = 2, padx = 2)


# Run app
app = LungXapp()
app.mainloop()
