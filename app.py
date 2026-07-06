from tkinter import *
from main import run

# Class for creating a new window
class NewWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("New Window")
        self.geometry("250x150")

        Label(self, text="This is a new window").pack(pady=20)
        T = Text(self, height = 5, width = 52)
        T.pack()
    
        #run()

# Create the main window
master = Tk()
master.geometry("300x200")
master.title("Main Window")

Label(master, text="This is the main window").pack(pady=10)

# Create a button to open the new window using the class
btn = Button(master, text="Open New Window")
btn.bind("<Button>", lambda e: NewWindow(master))  # Bind the event

btn.pack(pady=10)

# Run the Tkinter event loop
master.mainloop()