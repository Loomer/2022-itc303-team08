import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime

LARGE_FONT = ("Verdana", 16)

img_path = ''

dateTimeObj = datetime.now()

class LungXapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "LungX")
        tk.Tk.wm_geometry(self, '800x450')

        container = tk.Frame(self)
        
        container.pack(side = "top", fill = "both", expand = "True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ResultsPage, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        title = tk.Label(self, text="LungX", font=LARGE_FONT)
        title.place(relx=.5, rely=.1,anchor= tk.CENTER)

        filename_label = tk.Label(self, text = '')

        upload_button = ttk.Button(self, text="Upload File...",
                                   command=lambda:[

                                       select_file(),
                                       filename_label.config(text = img_path),
                                       filename_label.place(relx=.5, rely=.6,anchor= tk.CENTER),
                                       upload_button.place(relx=.4, rely=.7,anchor= tk.CENTER),
                                       analyse_button.place(relx=.6, rely=.7,anchor= tk.CENTER)
                                       ])
        
        analyse_button = ttk.Button(self, text="Analyse Image...",
                            command=lambda: controller.show_frame(ResultsPage))
        
        upload_button.place(relx=.5, rely=.7,anchor= tk.CENTER)

 

def select_file():
    filetypes = (
        ('JPEG', '*.jpg'),
        ('JPEG', '*.jpeg'),
        ('PNG', '*.png'),
        ('Images', '*.jpg'),
        ('Images', '*.jpeg'),
        ('Images', '*.png'),
    )

    
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/Pictures',
        filetypes=filetypes)

    global img_path
    img_path = filename


##    showinfo(
##        title='Selected File',
##        message=filename
##    )

class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = tk.Label(self, text="Severity Report", font=LARGE_FONT)
        title.place(relx=.5, rely=.1,anchor= tk.CENTER)

        severity_label = tk.Label(self, text="Severity Score: ")
        severity_label.place(relx=.5, rely=.7,anchor= tk.CENTER)

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
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.grid(row = 0, column = 0, pady = 2, padx = 2)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row = 1, column = 0, pady = 2, padx = 2)

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(ResultsPage))
        button2.grid(row = 2, column = 0, pady = 2, padx = 2)



app = LungXapp()
app.mainloop()
