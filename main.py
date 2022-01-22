# Gearbox Selection

""" 
This program is to take a basic set of mechanical info, for both the input and output of the setup,
And recommend a gearbox and motor combination that will provide the requested outputs
"""


from FrameRecommend import *
from FrameCheck import *
import tkinter as tk
from tkinter import ttk


class Window:
    def __init__(self, root, title, geometry):
        # This will set all the base information to make the main window
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        # Universal variables
        pad_ext = 5
        pad_int = 2
        entry_width = 10

        # This will create the main notebook for the entire program
        notebook_main = ttk.Notebook(master=root)
        notebook_main.pack(expand=1, fill='both', padx=pad_ext, pady=pad_ext)

        # To create the frames for each main tab
        tab_checkspecs = tk.Frame(master=notebook_main)
        tab_recommend = tk.Frame(master=notebook_main)
        # And to add them to the main notebook
        notebook_main.add(tab_checkspecs, text='Check Geared Motor')
        notebook_main.add(tab_recommend, text='Recommend Geared Motor')

        # Putting all the frames into the main program now
        frame_recommend = FrameRecommend(tab_recommend)

        self.root.mainloop()  # To actually run the program loop


def main():
    window = Window(tk.Tk(), 'Gearbox Selection', '1000x900')  # Main window defined here


main()
