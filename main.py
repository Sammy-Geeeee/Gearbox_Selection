# Gearbox Selection 1.1

# This program is an upgrade to the previous gearbox selection program, just making it into a GUI program.
# This will take a handful of inputs and output recommendations for the type of gearbox for that application


from functions import *
import tkinter as tk
from tkinter import ttk
from tkinter import font


def main():  # This function will be for executing the entire program
    root = tk.Tk()  # To define the main window object
    window = Window(root, 'Gearbox Selection', '1500x500')


class Window:  # Defines the class for the entire window
    def __init__(self, root, title, geometry):
        # This will set all the base information to make the main window
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure([0, 2], weight=1)

        # This will be all the universal variables
        pad_ext = 5
        pad_int = 2

        # This will set all the primary frames and their information
        frame_inputs = tk.Frame(self.root)
        in_out_separator = ttk.Separator(self.root, orient='vertical')
        frame_outputs = tk.Frame(self.root)
        label_inputs = tk.Label(self.root, text='Input Information')
        label_output = tk.Label(self.root, text='Gearbox Recommendations')

        frame_inputs.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)  # This will be all the positioning
        in_out_separator.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=pad_ext, pady=pad_ext)
        frame_outputs.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        label_inputs.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        label_output.grid(row=0, column=2, padx=pad_ext, pady=(pad_ext, 0))

        # This sets all the information for the widgets in the input frame
        frame_inputs.columnconfigure([1, 3], weight=1)
        frame_outputs.columnconfigure(0, weight=1)
        frame_outputs.rowconfigure(0, weight=1)
        type_menu_choices = ['Select Type', 'VF W']
        self.type_menu_value = tk.StringVar(frame_inputs)

        label_type = tk.Label(frame_inputs, text='Type')
        label_spd = tk.Label(frame_inputs, text='Output Speed (rpm)')
        label_spd_tol = tk.Label(frame_inputs, text='Tolerance (%)')
        label_tor = tk.Label(frame_inputs, text='Output Torque (Nm)')
        label_tor_tol = tk.Label(frame_inputs, text='Tolerance (%)')
        label_shft_min = tk.Label(frame_inputs, text='Min. Shaft (mm)')
        label_shft_max = tk.Label(frame_inputs, text='Max. Shaft (mm)')
        menu_type = ttk.OptionMenu(frame_inputs, self.type_menu_value, *type_menu_choices)
        button_calculate = tk.Button(frame_inputs, text='Calculate', command=self.calculate_gearboxes)
        self.entry_spd = tk.Entry(frame_inputs)
        self.entry_spd_tol = tk.Entry(frame_inputs)
        self.entry_tor = tk.Entry(frame_inputs)
        self.entry_tor_tol = tk.Entry(frame_inputs)
        self.entry_shft_min = tk.Entry(frame_inputs)
        self.entry_shft_max = tk.Entry(frame_inputs)

        label_type.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)  # This will be all the positioning
        label_spd.grid(row=1, column=0, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        label_spd_tol.grid(row=1, column=2, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        label_tor.grid(row=2, column=0, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        label_tor_tol.grid(row=2, column=2, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        label_shft_min.grid(row=3, column=0, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        label_shft_max.grid(row=3, column=2, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        menu_type.grid(row=0, column=1, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        button_calculate.grid(row=0, column=3, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        self.entry_spd.grid(row=1, column=1, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        self.entry_spd_tol.grid(row=1, column=3, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        self.entry_tor.grid(row=2, column=1, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        self.entry_tor_tol.grid(row=2, column=3, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        self.entry_shft_min.grid(row=3, column=1, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)
        self.entry_shft_max.grid(row=3, column=3, padx=pad_ext, pady=pad_ext, ipadx=pad_int, ipady=pad_int)

        # This is all the information for the output frame
        list_font = font.Font(size=12)
        self.list_reco = tk.Listbox(frame_outputs, width=100, height=200)
        self.list_reco.config(font=list_font)

        self.list_reco.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E, padx=(pad_ext, 2*pad_ext), pady=(pad_ext, 2*pad_ext), ipadx=pad_int, ipady=pad_int)

        self.root.mainloop()

    def calculate_gearboxes(self):
        self.list_reco.delete(0, tk.END)
        inputs = {
            'type': str(self.type_menu_value.get()),
            'out_spd': float(self.entry_spd.get()),
            'out_trq': float(self.entry_tor.get()),
            'shft_min': float(self.entry_shft_min.get()),
            'shft_max': float(self.entry_shft_max.get()),
            'tol_spd': float(self.entry_spd_tol.get()),
            'tol_trq': float(self.entry_tor_tol.get())
        }

        options = entire_function(inputs)

        for option in sorted(options):
            self.list_reco.insert(tk.END, option[0])
            self.list_reco.insert(tk.END, option[1])
            if option[2] != '':
                self.list_reco.insert(tk.END, option[2])
            self.list_reco.insert(tk.END, '')


main()  # Running the everything function

# End - 11/05/2021

# FUTURE WORK OR FURTHER ITERATIONS
# Make the gearbox type multi-selectable, and choose from all the specified options
# Add in a box where you can choose the motor poles, so you can have just 4 poles or all options as is
# Make each of the final selections an object, so you can then get a full part number and specification from there
# Could provide a somewhat design report, like the Gates Belt program
# This does a blanket exclusion of all gearboxes not rated for the torque, but even if they don't actually require that amount. Adjust this to be better
# This also changes the ratings when you alter the tolerance, which I don't think it should be doing. Ratings should be fixed, tolerance is only for selection
# General accuracy and whatnot of this could be improved, need to figure out how to do this better
# TODO - The efficiency spec is only given for worms, but I think it is already taken into account in the stats in the torque tables
# TODO -    So you will need to remove this part from the program as it's actually irrelevant, will have to make sure I have this right before more mofifications
