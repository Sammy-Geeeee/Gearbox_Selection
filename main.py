# Gearbox Selection

""" 
This program is to take a basic set of mechanical info, for both the input and output of the setup,
And recommend a gearbox and motor combination that will provide the requested outputs
"""


import openpyxl
import tkinter as tk
from tkinter import ttk
from tkinter import font
from ttkwidgets import CheckboxTreeview


def main():
    root = tk.Tk()  # To define the main window object
    window = Window(root, 'Gearbox Selection', '1500x750')  # Window size and name defined here

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

        # This will set all the primary frames and their information
        label_inputs = tk.Label(self.root, text='Input Information')
        frame_inputs = tk.Frame(self.root)
        separator_in_out = ttk.Separator(self.root, orient='vertical')
        label_output = tk.Label(self.root, text='Output Information')
        frame_outputs = tk.Frame(self.root)
        separator_out_reco = ttk.Separator(self.root, orient='vertical')
        label_reco = tk.Label(self.root, text='Gearbox Recommendations')
        frame_reco = tk.Frame(self.root)
        # This will be all the positioning for these primary frames
        label_inputs.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        frame_inputs.grid(row=1, column=0)
        separator_in_out.grid(row=0, column=1, rowspan=2, padx=pad_ext, pady=pad_ext, sticky='nsew')
        label_output.grid(row=0, column=2, padx=pad_ext, pady=pad_ext)
        frame_outputs.grid(row=1, column=2)
        separator_out_reco.grid(row=0, column=3, rowspan=2, padx=pad_ext, pady=pad_ext, sticky='nsew')
        label_reco.grid(row=0, column=4, padx=pad_ext, pady=pad_ext)
        frame_reco.grid(row=1, column=4)

        # Widgets in the input frame
        label_option_tree = tk.Label(frame_inputs, text="Applicable Series")
        scroll_series = tk.Scrollbar(frame_inputs)
        option_tree = CheckboxTreeview(frame_inputs, yscrollcommand=scroll_series.set)
        scroll_series.config(command=option_tree.yview)
        separator_input1 = ttk.Separator(frame_inputs, orient='horizontal')
        label_motor_info = tk.Label(frame_inputs, text='Motor Input')
        label_power = tk.Label(frame_inputs, text='Power')
        entry_power = tk.Entry(frame_inputs, width=entry_width)
        units = ['test', 'one', '2']  # TODO - FIX THIS TO BE APPROPRIATE LATER ON
        menu_power = ttk.OptionMenu(frame_inputs, tk.StringVar(frame_inputs), *units)
        label_poles = tk.Label(frame_inputs, text='Poles')
        poles = ['two', '4', 6, 'Eight']  # TODO - FIX THIS LATER ON
        menu_poles = ttk.OptionMenu(frame_inputs, tk.StringVar(frame_inputs), *poles)
        # Info for position of these here
        label_option_tree.grid(row=0, column=0, columnspan=3, padx=pad_ext, pady=pad_ext)
        scroll_series.grid(row=1, column=2, padx=pad_ext, pady=pad_ext, sticky='ns')
        option_tree.grid(row=1, column=0, columnspan=2, padx=pad_ext, pady=pad_ext)
        separator_input1.grid(row=2, column=0, columnspan=3, padx=pad_ext, pady=pad_ext, sticky='nsew')
        label_motor_info.grid(row=3, column=0, columnspan=3)
        label_power.grid(row=4, column=0, padx=pad_ext, pady=pad_ext)
        entry_power.grid(row=4, column=1, padx=pad_ext, pady=pad_ext)
        menu_power.grid(row=4, column=2, padx=pad_ext, pady=pad_ext)
        label_poles.grid(row=5, column=0, padx=pad_ext, pady=pad_ext)
        menu_poles.grid(row=5, column=2, padx=pad_ext, pady=pad_ext)

        # This code is to generate all the series and sizes in the selection tree
        series_sizes = {'VF_W':[], 'A':[], 'C':[], 'F':[]}
        for series_size in series_sizes:
            workbook = openpyxl.load_workbook(f'{series_size}_Gearboxes.xlsx')
            sheets =  workbook.worksheets
            for sheet in sheets:
                series_size_name = sheet['A2'].value
                series_size_shaft = sheet['O1'].value
                series_size_shaft_alt = sheet['P1'].value
                if series_size_shaft_alt is not None:
                    series_sizes[series_size].append(f'{series_size_name}    ({series_size_shaft}mm, {series_size_shaft_alt}mm)')
                else:
                    series_sizes[series_size].append(f'{series_size_name}    ({series_size_shaft}mm)')
        # To insert all these sizes into the tree
        for key in series_sizes:
            option_tree.insert('', 'end', key, text=key)
            for value in series_sizes[key]:
                option_tree.insert(key, 'end', value, text=value)

        # Output frame widgets here
        label_speed = tk.Label(frame_outputs, text="Speed")
        entry_speed = tk.Entry(frame_outputs, width=entry_width)
        options_speed = ['test', 'one', '2']  # TODO - FIX THIS TO BE APPROPRIATE LATER ON
        menu_speed = ttk.OptionMenu(frame_outputs, tk.StringVar(frame_outputs), *options_speed)
        label_torque = tk.Label(frame_outputs, text="Torque")
        entry_torque = tk.Entry(frame_outputs, width=entry_width)
        options_torque = ['test', 'one', '2']  # TODO - FIX THIS TO BE APPROPRIATE LATER ON
        menu_torque = ttk.OptionMenu(frame_outputs, tk.StringVar(frame_outputs), *options_torque)
        label_safety = tk.Label(frame_outputs, text='Safety Factor')
        entry_safety = tk.Entry(frame_outputs, width=entry_width)
        # And positional info for all these widgets
        label_speed.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        entry_speed.grid(row=0, column=1, padx=pad_ext, pady=pad_ext)
        menu_speed.grid(row=0, column=2, padx=pad_ext, pady=pad_ext)
        label_torque.grid(row=1, column=0, padx=pad_ext, pady=pad_ext)
        entry_torque.grid(row=1, column=1, padx=pad_ext, pady=pad_ext)
        menu_torque.grid(row=1, column=2, padx=pad_ext, pady=pad_ext)
        label_safety.grid(row=2, column=0, padx=pad_ext, pady=pad_ext)
        entry_safety.grid(row=2, column=1, padx=pad_ext, pady=pad_ext)

        # Gearbox recommendations widgets here
        scroll_list = tk.Scrollbar(frame_reco)
        list_reco = tk.Listbox(frame_reco, yscrollcommand=scroll_list.set, width=40, height=10)
        scroll_list.config(command=list_reco.yview)
        button_reco = tk.Button(frame_reco, text='Generate Recommendations', command="")  # TODO - Change the command to an actual function

        # And positioning info
        scroll_list.grid(row=0, column=1, sticky='ns')
        list_reco.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky='nsew')
        button_reco.grid(row=1, column=0, padx=pad_ext, pady=pad_ext)



        
        
        








        self.root.mainloop()





main()


















# class Window:
#     def __init__(self, root, title, geometry):
#         
#         

#         

#         self.root.mainloop()

#     def calculate_gearboxes(self):
#         self.list_reco.delete(0, tk.END)
#         inputs = {
#             'type': str(self.type_menu_value.get()),
#             'out_spd': float(self.entry_spd.get()),
#             'out_trq': float(self.entry_tor.get()),
#             'shft_min': float(self.entry_shft_min.get()),
#             'shft_max': float(self.entry_shft_max.get()),
#             'tol_spd': float(self.entry_spd_tol.get()),
#             'tol_trq': float(self.entry_tor_tol.get())
#         }

#         options = entire_function(inputs)

#         for option in sorted(options):
#             self.list_reco.insert(tk.END, option[0])
#             self.list_reco.insert(tk.END, option[1])
#             if option[2] != '':
#                 self.list_reco.insert(tk.END, option[2])
#             self.list_reco.insert(tk.END, '')



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
