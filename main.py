# Gearbox Selection

""" 
This program is to take a basic set of mechanical info, for both the input and output of the setup,
And recommend a gearbox and motor combination that will provide the requested outputs
"""

from functions import *
import string
import re
import openpyxl
import tkinter as tk
from tkinter import ttk
from ttkwidgets import CheckboxTreeview


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
        self.label_inputs = tk.Label(self.root, text='Input Information')
        self.frame_inputs = tk.Frame(self.root)
        self.separator_in_out = ttk.Separator(self.root, orient='vertical')
        self.label_output = tk.Label(self.root, text='Output Information')
        self.frame_outputs = tk.Frame(self.root)
        self.separator_out_reco = ttk.Separator(self.root, orient='vertical')
        self.label_reco = tk.Label(self.root, text='Gearbox Recommendations')
        self.frame_reco = tk.Frame(self.root)
        # This will be all the positioning for these primary frames
        self.label_inputs.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        self.frame_inputs.grid(row=1, column=0)
        self.separator_in_out.grid(row=0, column=1, rowspan=2, padx=pad_ext, pady=pad_ext, sticky='nsew')
        self.label_output.grid(row=0, column=2, padx=pad_ext, pady=pad_ext)
        self.frame_outputs.grid(row=1, column=2)
        self.separator_out_reco.grid(row=0, column=3, rowspan=2, padx=pad_ext, pady=pad_ext, sticky='nsew')
        self.label_reco.grid(row=0, column=4, padx=pad_ext, pady=pad_ext)
        self.frame_reco.grid(row=1, column=4)

        # Widgets in the input frame
        self.label_option_tree = tk.Label(self.frame_inputs, text="Applicable Series/Sizes")
        self.scroll_tree = tk.Scrollbar(self.frame_inputs)
        self.option_tree = CheckboxTreeview(self.frame_inputs, yscrollcommand=self.scroll_tree.set)
        self.scroll_tree.config(command=self.option_tree.yview)
        self.separator_input1 = ttk.Separator(self.frame_inputs, orient='horizontal')
        self.label_motor_info = tk.Label(self.frame_inputs, text='Motor Input')
        self.label_power = tk.Label(self.frame_inputs, text='Power')
        self.entry_power = tk.Entry(self.frame_inputs, width=entry_width)
        self.units = ['test', 'one', '2']  # TODO - FIX THIS TO BE APPROPRIATE LATER ON
        self.stringvar_power = tk.StringVar(self.frame_inputs)
        self.menu_power = ttk.OptionMenu(self.frame_inputs, self.stringvar_power, *self.units)
        self.label_poles = tk.Label(self.frame_inputs, text='Poles')
        self.poles = [None, '2', '4', '6', '8']
        self.stringvar_poles = tk.StringVar(self.frame_inputs)
        self.menu_poles = ttk.OptionMenu(self.frame_inputs, self.stringvar_poles, self.poles[0], *self.poles)
        # Info for position of these here
        self.label_option_tree.grid(row=0, column=0, columnspan=3, padx=pad_ext, pady=pad_ext)
        self.scroll_tree.grid(row=1, column=2, padx=pad_ext, pady=pad_ext, sticky='ns')
        self.option_tree.grid(row=1, column=0, columnspan=2, padx=pad_ext, pady=pad_ext)
        self.separator_input1.grid(row=2, column=0, columnspan=3, padx=pad_ext, pady=pad_ext, sticky='nsew')
        self.label_motor_info.grid(row=3, column=0, columnspan=3)
        self.label_power.grid(row=4, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_power.grid(row=4, column=1, padx=pad_ext, pady=pad_ext)
        self.menu_power.grid(row=4, column=2, padx=pad_ext, pady=pad_ext)
        self.label_poles.grid(row=5, column=0, padx=pad_ext, pady=pad_ext)
        self.menu_poles.grid(row=5, column=2, padx=pad_ext, pady=pad_ext)

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
            self.option_tree.insert('', 'end', key, text=key)
            for value in series_sizes[key]:
                self.option_tree.insert(key, 'end', value, text=value)

        # Output frame widgets here
        self.label_speed = tk.Label(self.frame_outputs, text='Speed')
        self.entry_speed = tk.Entry(self.frame_outputs, width=entry_width)
        self.options_speed = ['test', 'one', '2']  # TODO - FIX THIS TO BE APPROPRIATE LATER ON
        self.stringvar_speed = tk.StringVar(self.frame_outputs)
        self.menu_speed = ttk.OptionMenu(self.frame_outputs, self.stringvar_speed, *self.options_speed)
        self.label_spd_updown = tk.Label(self.frame_outputs, text='+/-')
        self.entry_spd_tol = tk.Entry(self.frame_outputs, width=entry_width)
        self.label_spd_perc = tk.Label(self.frame_outputs, text='%')
        self.label_torque = tk.Label(self.frame_outputs, text="Torque")
        self.entry_torque = tk.Entry(self.frame_outputs, width=entry_width)
        self.options_torque = ['test', 'one', '2']  # TODO - FIX THIS TO BE APPROPRIATE LATER ON
        self.stringvar_torque = tk.StringVar(self.frame_outputs)
        self.menu_torque = ttk.OptionMenu(self.frame_outputs, self.stringvar_torque, *self.options_torque)
        self.label_trq_updown = tk.Label(self.frame_outputs, text='+/-')
        self.entry_trq_tol = tk.Entry(self.frame_outputs, width=entry_width)
        self.label_trq_perc = tk.Label(self.frame_outputs, text='%')
        self.label_safety = tk.Label(self.frame_outputs, text='Safety Factor')
        self.entry_safety = tk.Entry(self.frame_outputs, width=entry_width)
        # And positional info for all these widgets
        self.label_speed.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_speed.grid(row=0, column=1, padx=pad_ext, pady=pad_ext)
        self.menu_speed.grid(row=0, column=2, padx=pad_ext, pady=pad_ext)
        self.label_spd_updown.grid(row=0, column=3, padx=pad_ext, pady=pad_ext)
        self.entry_spd_tol.grid(row=0, column=4, padx=pad_ext, pady=pad_ext)
        self.label_spd_perc.grid(row=0, column=5, padx=pad_ext, pady=pad_ext)
        self.label_torque.grid(row=1, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_torque.grid(row=1, column=1, padx=pad_ext, pady=pad_ext)
        self.menu_torque.grid(row=1, column=2, padx=pad_ext, pady=pad_ext)
        self.label_trq_updown.grid(row=1, column=3, padx=pad_ext, pady=pad_ext)
        self.entry_trq_tol.grid(row=1, column=4, padx=pad_ext, pady=pad_ext)
        self.label_trq_perc.grid(row=1, column=5, padx=pad_ext, pady=pad_ext)
        self.label_safety.grid(row=2, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_safety.grid(row=2, column=1, padx=pad_ext, pady=pad_ext)

        # Gearbox recommendations widgets here
        self.scroll_list = tk.Scrollbar(self.frame_reco)
        self.list_reco = tk.Listbox(self.frame_reco, yscrollcommand=self.scroll_list.set, width=40, height=10)
        self.scroll_list.config(command=self.list_reco.yview)
        self.button_reco = tk.Button(self.frame_reco, text='Generate Recommendations', command=lambda: do_something(self.retrieve_inputs()))  # TODO - Change the command to an actual function, to use function with inputs... command=lambda: function(input)
        # And positioning info
        self.scroll_list.grid(row=0, column=1, sticky='ns')
        self.list_reco.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky='nsew')
        self.button_reco.grid(row=1, column=0, padx=pad_ext, pady=pad_ext)

        self.root.mainloop()
    

    def retrieve_inputs(self):
        motor_power = self.entry_power.get()
        motor_power_unit = self.stringvar_power.get()
        motor_poles = self.stringvar_poles.get()
        output_speed = self.entry_speed.get()
        output_speed_unit = self.stringvar_speed.get()
        output_speed_tol = self.entry_spd_tol.get()
        output_torque = self.entry_torque.get()
        output_torque_unit = self.stringvar_torque.get()
        output_torque_tol = self.entry_trq_tol.get()
        safety_factor = self.entry_safety.get()
        series_sizes = self.option_tree.get_checked()  # To get checked items from tree
        # Below code is to take tree inputs and turn them into a useful dictionary
        applicable_series_sizes = {'VF_W':[], 'A':[], 'C':[], 'F':[]}
        replacement = str.maketrans(string.punctuation, ' '*32)
        for serie_size in series_sizes:
            no_punc = serie_size.translate(replacement)
            name = re.search(r'[A-Z]+ [A-Z]+ [0-9]+ [0-9]+|[A-Z]+ [0-9]+', no_punc).group()
            if (name[0] == 'V' or name[0] == 'W'):
                applicable_series_sizes['VF_W'].append(name)
            elif (name[0] == 'A'):
                applicable_series_sizes['A'].append(name)
            elif (name[0] == 'C'):
                applicable_series_sizes['C'].append(name)
            elif (name[0] == 'F'):
                applicable_series_sizes['F'].append(name)

        return {
            'series sizes': applicable_series_sizes,
            'power': motor_power,
            'power unit': motor_power_unit,
            'poles': motor_poles,
            'speed': output_speed,
            'speed unit': output_speed_unit,
            'speed tol': output_speed_tol,
            'torque': output_torque,
            'torque unit': output_torque_unit,
            'torque tol': output_torque_tol,
            'safety factor': safety_factor
        }


    def show_recommendations(self):
        pass
        # self.list_reco.delete(0, tk.END)
        # inputs = {
        #     'type': str(self.type_menu_value.get()),
        #     'out_spd': float(self.entry_spd.get()),
        #     'out_trq': float(self.entry_tor.get()),
        #     'shft_min': float(self.entry_shft_min.get()),
        #     'shft_max': float(self.entry_shft_max.get()),
        #     'tol_spd': float(self.entry_spd_tol.get()),
        #     'tol_trq': float(self.entry_tor_tol.get())
        # }

        # options = entire_function(inputs)

        # for option in sorted(options):
        #     self.list_reco.insert(tk.END, option[0])
        #     self.list_reco.insert(tk.END, option[1])
        #     if option[2] != '':
        #         self.list_reco.insert(tk.END, option[2])
        #     self.list_reco.insert(tk.END, '')


def main():
    root = tk.Tk()  # To define the main window object
    window = Window(root, 'Gearbox Selection', '1500x750')  # Window size and name defined here





main()













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
